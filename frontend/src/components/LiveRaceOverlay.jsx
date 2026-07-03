import { useEffect, useMemo, useRef, useState } from "react";

/**
 * LiveRaceOverlay - fullscreen animated race broadcast.
 *
 * Props:
 *   circuit: string
 *   round: number
 *   drivers: [{name, team, rating}]   (season roster)
 *   race: object | null               (backend result — appears mid-animation)
 *   onDone: () => void                (called when the closing button is pressed)
 *   totalLaps: number (default 40)
 *   speedMs: number   (ms per lap tick; default 320)
 */

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
const TEAM_PALETTE = [
  "#E4FF00", "#FF3B30", "#00F0FF", "#00FF66", "#FF66C4", "#FFA500",
  "#8A5CFF", "#F8F8F8", "#FFD500", "#22B573", "#FF8080", "#59B4FF",
  "#DE00A5", "#FF4E00", "#B0E000", "#7BE3FF", "#FF9E7A", "#C9A26D",
  "#00C48C", "#FF5CA0", "#4EA8FF", "#FFB84D", "#9AF200", "#FF3D68",
];

const hashCode = (s = "") => {
  let h = 0;
  for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return Math.abs(h);
};
const teamColor = (team) => TEAM_PALETTE[hashCode(team) % TEAM_PALETTE.length];
const initials = (name = "") =>
  name
    .split(" ")
    .filter(Boolean)
    .map((p) => p[0])
    .join("")
    .slice(0, 3)
    .toUpperCase();
const surname = (name = "") => {
  const parts = name.split(" ").filter(Boolean);
  return parts[parts.length - 1] || name;
};

// Deterministic-ish RNG (mulberry32) so replays feel stable per race
const makeRng = (seed) => {
  let a = seed || 1;
  return () => {
    a |= 0;
    a = (a + 0x6D2B79F5) | 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
};

// Build a starting grid based on driver rating + small qualifying noise.
const buildQualifyingGrid = (drivers, seed) => {
  const rng = makeRng(seed || 42);
  const scored = drivers.map((d) => ({
    ...d,
    q: (d.rating || 70) + (rng() - 0.5) * 12,
  }));
  scored.sort((a, b) => b.q - a.q);
  return scored.map((d, i) => ({ ...d, gridPos: i + 1 }));
};

// Turn discrete backend results into an ordered final grid (DNFs at the bottom).
const buildFinalOrder = (race, roster) => {
  if (!race) return null;
  const byName = {};
  race.results.forEach((r, i) => {
    byName[r.driver] = { ...r, finalIdx: i };
  });
  // Any roster driver missing from results (shouldn't happen) -> park at bottom
  const missing = roster.filter((d) => !byName[d.name]);
  const finalDrivers = [
    ...race.results.map((r, i) => ({
      name: r.driver,
      team: r.team,
      dnf: r.dnf,
      points: r.points,
      finalPos: i + 1,
    })),
    ...missing.map((d, i) => ({
      name: d.name,
      team: d.team,
      dnf: true,
      points: 0,
      finalPos: race.results.length + i + 1,
    })),
  ];
  return finalDrivers;
};

// Choose a DNF lap for each driver flagged dnf.
const scheduleDnfs = (finalOrder, totalLaps, rng) => {
  const map = {};
  finalOrder.forEach((d) => {
    if (d.dnf) {
      // spread DNFs across race (5 - totalLaps-2)
      map[d.name] = Math.max(4, Math.floor(rng() * (totalLaps - 6)) + 3);
    }
  });
  return map;
};

// Given lap progress 0..1, interpolate driver order from grid -> final.
// We use a smooth-step so most swaps happen mid-race.
const interpolateOrder = (grid, finalOrder, dnfLap, lap, totalLaps) => {
  const t = Math.min(1, Math.max(0, lap / totalLaps));
  // ease-in-out
  const e = t * t * (3 - 2 * t);
  const finalIdxByName = {};
  finalOrder.forEach((d, i) => (finalIdxByName[d.name] = i));

  // Cars still running
  const running = [];
  const retired = [];
  grid.forEach((d, i) => {
    const dnfL = dnfLap[d.name];
    if (dnfL && lap >= dnfL) {
      retired.push({ ...d, retiredAt: dnfL });
    } else {
      const finalIdx =
        finalIdxByName[d.name] === undefined ? i : finalIdxByName[d.name];
      const interp = i * (1 - e) + finalIdx * e;
      running.push({ ...d, _interp: interp + (d.gridPos % 2) * 0.001 });
    }
  });
  running.sort((a, b) => a._interp - b._interp);
  return { running, retired };
};

// ---------------------------------------------------------------------------
// Track SVG (stylised oval-ish figure-eight-ish path)
// ---------------------------------------------------------------------------
const TRACK_PATH =
  "M 90 200 C 90 90, 220 60, 360 90 C 500 120, 560 60, 700 90 C 830 118, 900 200, 830 280 C 760 355, 600 300, 470 320 C 340 340, 230 380, 140 330 C 60 285, 90 260, 90 200 Z";
const TRACK_LENGTH = 1900; // approximate for path length usage

const TrackDot = ({ pct, color, label, dim, glow }) => {
  return (
    <g transform={`translate(-9,-9)`}>
      <circle
        r={dim ? 5 : 7}
        fill={color}
        stroke="#0A0A0A"
        strokeWidth="2"
        style={{
          filter: glow
            ? `drop-shadow(0 0 6px ${color})`
            : "drop-shadow(0 0 2px rgba(0,0,0,0.6))",
        }}
      />
      <text
        x={12}
        y={4}
        fill="#F2F2F2"
        fontSize="10"
        style={{ fontFamily: "JetBrains Mono, monospace", fontWeight: 700 }}
      >
        {label}
      </text>
    </g>
  );
};

// ---------------------------------------------------------------------------
// Main component
// ---------------------------------------------------------------------------
const LiveRaceOverlay = ({
  circuit,
  round,
  drivers,
  race,
  onDone,
  totalLaps = 40,
  speedMs = 320,
}) => {
  const [lap, setLap] = useState(0);
  const [feed, setFeed] = useState([]); // {t, kind, text}
  const [state, setState] = useState("pre"); // pre | running | flag | done
  const [showResults, setShowResults] = useState(false);

  // Freeze race prop into a ref once received so animation is deterministic
  const raceRef = useRef(race);
  useEffect(() => {
    if (race && !raceRef.current) raceRef.current = race;
  }, [race]);

  const seed = useMemo(() => hashCode(circuit + round), [circuit, round]);
  const rng = useMemo(() => makeRng(seed + 7), [seed]);
  const grid = useMemo(
    () => buildQualifyingGrid(drivers, seed),
    [drivers, seed]
  );

  const finalOrder = useMemo(
    () => (race ? buildFinalOrder(race, drivers) : null),
    [race, drivers]
  );
  const dnfLap = useMemo(
    () => (finalOrder ? scheduleDnfs(finalOrder, totalLaps, rng) : {}),
    [finalOrder, totalLaps, rng]
  );

  // formation lap intro
  useEffect(() => {
    setFeed([
      {
        t: 0,
        kind: "flag",
        text: `Formation lap em ${circuit}. Grid alinhado — pole para ${surname(
          grid[0].name
        )} (${grid[0].team}).`,
      },
    ]);
    const t1 = setTimeout(() => {
      setFeed((f) => [
        ...f,
        { t: 0, kind: "green", text: `BANDEIRA VERDE — largada!` },
      ]);
      setState("running");
    }, 1400);
    return () => clearTimeout(t1);
  }, [circuit, grid]);

  // Lap tick
  useEffect(() => {
    if (state !== "running") return;
    if (lap >= totalLaps) return;
    const timer = setTimeout(() => setLap((l) => l + 1), speedMs);
    return () => clearTimeout(timer);
  }, [state, lap, totalLaps, speedMs]);

  // Snapshot at each lap => detect overtakes/DNFs/etc
  const prevOrder = useRef(grid.map((d) => d.name));
  useEffect(() => {
    if (state !== "running" || lap === 0) return;

    const r = raceRef.current;
    const fo = r ? buildFinalOrder(r, drivers) : null;
    if (!fo) return;
    const { running, retired } = interpolateOrder(
      grid,
      fo,
      dnfLap,
      lap,
      totalLaps
    );
    const currentNames = running.map((d) => d.name);

    // Detect DNFs happening at this exact lap
    Object.entries(dnfLap).forEach(([name, dl]) => {
      if (dl === lap) {
        const drv = drivers.find((d) => d.name === name);
        const reasons = [
          "problema mecânico",
          "abandono no boxes",
          "toque na dianteira",
          "roda solta",
          "quebra de câmbio",
          "motor superaquecido",
          "acidente na S do Senna",
          "erro no pitlane",
        ];
        const rr = reasons[Math.floor(rng() * reasons.length)];
        setFeed((f) => [
          ...f,
          {
            t: lap,
            kind: "dnf",
            text: `V${lap} — DNF: ${surname(name)} (${drv?.team || ""}) — ${rr}.`,
          },
        ]);
      }
    });

    // Detect overtakes — compare to previous order (only top 10 to avoid spam)
    const prev = prevOrder.current;
    const topN = 8;
    for (let i = 0; i < Math.min(topN, currentNames.length); i++) {
      const now = currentNames[i];
      const prevPos = prev.indexOf(now);
      if (prevPos > i && prevPos !== -1) {
        // gained positions
        const overtaken = prev[i];
        if (overtaken && overtaken !== now && rng() > 0.55) {
          const verbs = [
            "ultrapassa",
            "passa por dentro em",
            "assume a posição de",
            "toma o lugar de",
            "faz a manobra em cima de",
          ];
          const v = verbs[Math.floor(rng() * verbs.length)];
          setFeed((f) => [
            ...f,
            {
              t: lap,
              kind: "overtake",
              text: `V${lap} — P${i + 1}: ${surname(now)} ${v} ${surname(
                overtaken
              )}.`,
            },
          ]);
        }
      }
    }

    // Random flavour: safety car, virtual, fastest lap, pit stops
    if (lap === Math.floor(totalLaps * 0.35) && rng() > 0.4) {
      setFeed((f) => [
        ...f,
        {
          t: lap,
          kind: "sc",
          text: `V${lap} — SAFETY CAR na pista. Pelotão reagrupa.`,
        },
      ]);
    }
    if (lap === Math.floor(totalLaps * 0.55)) {
      setFeed((f) => [
        ...f,
        {
          t: lap,
          kind: "pit",
          text: `V${lap} — Janela de pit stops aberta. Estratégias divergem.`,
        },
      ]);
    }
    if (lap === Math.floor(totalLaps * 0.75) && running[0]) {
      setFeed((f) => [
        ...f,
        {
          t: lap,
          kind: "fast",
          text: `V${lap} — VOLTA MAIS RÁPIDA: ${surname(
            running[0].name
          )} imprime o ritmo.`,
        },
      ]);
    }

    prevOrder.current = currentNames;

    if (lap === totalLaps) {
      const winner = running[0];
      setFeed((f) => [
        ...f,
        {
          t: lap,
          kind: "chequered",
          text: `🏁 BANDEIRADA! Vencedor: ${surname(winner?.name || "")} (${
            winner?.team || ""
          }).`,
        },
      ]);
      setState("flag");
      setTimeout(() => setShowResults(true), 900);
    }
  }, [lap, state, grid, drivers, dnfLap, totalLaps, rng]);

  // -------------------------------------------------------------------------
  // Render
  // -------------------------------------------------------------------------
  const r = raceRef.current || race;
  const fo = r ? buildFinalOrder(r, drivers) : null;
  const { running = [], retired = [] } = fo
    ? interpolateOrder(grid, fo, dnfLap, lap, totalLaps)
    : { running: grid, retired: [] };

  // Compute path positions for each running car (spread along track based on
  // rank + fractional offset — the leader is furthest along, backmarkers behind).
  // Add small jitter so it doesn't look like a train.
  const totalRunning = running.length || 1;
  const carsWithPct = running.map((d, i) => {
    const base = 1 - i / totalRunning;
    const jitter = ((hashCode(d.name) % 7) - 3) * 0.005;
    return { ...d, pct: (base + jitter + 1) % 1 };
  });

  const feedBottomRef = useRef(null);
  useEffect(() => {
    feedBottomRef.current?.scrollTo({
      top: feedBottomRef.current.scrollHeight,
      behavior: "smooth",
    });
  }, [feed]);

  const progressPct = (lap / totalLaps) * 100;

  return (
    <div
      className="fixed inset-0 z-[100] bg-black/95 backdrop-blur-md flex items-center justify-center p-2 sm:p-6"
      data-testid="live-race-overlay"
    >
      <div className="relative w-full max-w-[1400px] max-h-[95vh] border border-[#262626] bg-[#0A0A0A] flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="border-b border-[#262626] px-6 py-4 flex flex-wrap items-baseline justify-between gap-3">
          <div className="flex items-baseline gap-3">
            <span className="font-mono-num text-[#E4FF00] font-bold text-lg">
              R{String(round).padStart(2, "0")}
            </span>
            <span className="font-head font-black uppercase text-2xl tracking-tight">
              {circuit}
            </span>
            <span className="label text-neutral-500 hidden sm:inline">
              // LIVE
            </span>
          </div>
          <div className="flex items-center gap-4">
            <div className="font-mono-num text-sm">
              <span className="text-neutral-500">LAP</span>{" "}
              <span className="font-bold text-[#E4FF00]">
                {String(lap).padStart(2, "0")}
              </span>
              <span className="text-neutral-600">
                /{String(totalLaps).padStart(2, "0")}
              </span>
            </div>
            <div className="w-40 h-1.5 bg-[#1F1F1F] overflow-hidden">
              <div
                className="h-full bg-[#E4FF00] transition-all"
                style={{ width: `${progressPct}%` }}
              />
            </div>
            {state === "flag" && (
              <span className="label text-[#00FF66] animate-pulse">
                ✓ ENCERRADA
              </span>
            )}
          </div>
        </div>

        {/* Main body: track + leaderboard + feed */}
        <div className="flex-1 grid grid-cols-1 lg:grid-cols-12 gap-0 overflow-hidden">
          {/* Track visualisation */}
          <div className="lg:col-span-6 border-r border-[#262626] p-4 flex flex-col">
            <div className="label text-neutral-500 mb-2">// CIRCUITO</div>
            <div className="relative flex-1 min-h-[260px]">
              <svg
                viewBox="0 0 950 400"
                className="w-full h-full"
                preserveAspectRatio="xMidYMid meet"
              >
                {/* Track outer glow */}
                <path
                  d={TRACK_PATH}
                  fill="none"
                  stroke="#1a1a1a"
                  strokeWidth="28"
                  strokeLinecap="round"
                />
                <path
                  d={TRACK_PATH}
                  fill="none"
                  stroke="#2A2A2A"
                  strokeWidth="16"
                  strokeLinecap="round"
                />
                <path
                  d={TRACK_PATH}
                  fill="none"
                  stroke="#0A0A0A"
                  strokeWidth="1.5"
                  strokeDasharray="4 8"
                />
                {/* Start/finish line marker */}
                <g transform="translate(90,200)">
                  <rect x="-2" y="-14" width="4" height="28" fill="#E4FF00" />
                </g>

                {/* Cars */}
                {carsWithPct.map((d, i) => {
                  const pct = d.pct;
                  const c = teamColor(d.team);
                  const isLeader = i === 0;
                  return (
                    <CarOnTrack
                      key={d.name}
                      pct={pct}
                      color={c}
                      label={initials(d.name)}
                      leader={isLeader}
                      dim={i > 9}
                    />
                  );
                })}
              </svg>
            </div>
            <div className="mt-3 text-[10px] tracking-[0.22em] uppercase text-neutral-600 flex justify-between">
              <span>PITLANE</span>
              <span>DRS ATIVO</span>
              <span>{totalRunning} EM PISTA · {retired.length} DNF</span>
            </div>
          </div>

          {/* Leaderboard */}
          <div className="lg:col-span-3 border-r border-[#262626] p-4 overflow-y-auto">
            <div className="label text-[#E4FF00] mb-2">// TOP 10 AO VIVO</div>
            <div className="space-y-1">
              {running.slice(0, 10).map((d, i) => {
                const c = teamColor(d.team);
                const prevPos = prevOrder.current.indexOf(d.name);
                const delta = prevPos === -1 ? 0 : prevPos - i;
                return (
                  <div
                    key={d.name}
                    className={`flex items-center gap-2 px-2 py-1.5 border border-[#1A1A1A] bg-[#111] transition-all duration-500 ${
                      i === 0 ? "border-[#E4FF00] bg-[#141400]" : ""
                    }`}
                    style={{ transform: `translateY(0)` }}
                  >
                    <span className="font-mono-num text-neutral-500 text-xs w-5 text-right">
                      {String(i + 1).padStart(2, "0")}
                    </span>
                    <span
                      className="w-1.5 h-6 rounded-sm shrink-0"
                      style={{ backgroundColor: c }}
                    />
                    <span
                      className={`flex-1 font-head font-bold uppercase text-xs tracking-tight truncate ${
                        i === 0 ? "text-[#E4FF00]" : ""
                      }`}
                    >
                      {surname(d.name)}
                    </span>
                    <span className="font-mono-num text-[10px] text-neutral-500 truncate max-w-[60px]">
                      {d.team}
                    </span>
                    {delta !== 0 && (
                      <span
                        className={`font-mono-num text-[10px] ${
                          delta > 0 ? "text-[#00FF66]" : "text-[#FF3B30]"
                        }`}
                      >
                        {delta > 0 ? `▲${delta}` : `▼${Math.abs(delta)}`}
                      </span>
                    )}
                  </div>
                );
              })}
            </div>

            {retired.length > 0 && (
              <div className="mt-4">
                <div className="label text-neutral-500 mb-2">// DNF</div>
                <div className="space-y-1">
                  {retired.map((d) => (
                    <div
                      key={d.name}
                      className="flex items-center gap-2 px-2 py-1 border border-[#1A1A1A] text-neutral-600"
                    >
                      <span
                        className="w-1.5 h-4 rounded-sm shrink-0 opacity-40"
                        style={{ backgroundColor: teamColor(d.team) }}
                      />
                      <span className="font-head font-bold uppercase text-xs tracking-tight truncate">
                        {surname(d.name)}
                      </span>
                      <span className="ml-auto font-mono-num text-[9px]">
                        V{d.retiredAt}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>

          {/* News / Commentary feed */}
          <div className="lg:col-span-3 p-4 flex flex-col overflow-hidden">
            <div className="label text-[#00F0FF] mb-2">// TRANSMISSÃO</div>
            <div
              ref={feedBottomRef}
              className="flex-1 overflow-y-auto space-y-2 pr-1"
              data-testid="live-feed"
            >
              {feed.map((f, i) => (
                <FeedItem key={i} f={f} />
              ))}
              {state === "running" && feed.length < 2 && (
                <div className="text-neutral-500 text-xs italic">
                  Aguardando primeiras voltas...
                </div>
              )}
            </div>
          </div>
        </div>

        {/* Bottom bar */}
        <div className="border-t border-[#262626] px-4 py-3 flex flex-wrap items-center justify-between gap-2">
          <div className="text-[10px] tracking-[0.22em] uppercase text-neutral-600">
            {race
              ? "// DADOS SINCRONIZADOS COM O SIMULADOR"
              : "// SIMULANDO CORRIDA..."}
          </div>
          {state === "flag" ? (
            <button
              onClick={onDone}
              data-testid="live-close-button"
              className="bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs px-6 py-3 hover:bg-[#C6DB00]"
            >
              Ver Resultado Completo →
            </button>
          ) : (
            <button
              onClick={onDone}
              data-testid="live-skip-button"
              className="border border-[#262626] text-neutral-400 font-bold uppercase tracking-[0.22em] text-xs px-4 py-2 hover:border-neutral-500 hover:text-white"
            >
              Pular animação
            </button>
          )}
        </div>

        {/* Final flash */}
        {showResults && race?.podium?.length >= 1 && (
          <div className="absolute inset-x-0 top-1/2 -translate-y-1/2 pointer-events-none">
            <div className="bg-[#E4FF00] text-black text-center py-3 mx-8 shadow-2xl animate-pulse">
              <div className="label text-black">// VENCEDOR</div>
              <div className="font-head font-black uppercase text-3xl sm:text-5xl tracking-tighter">
                {race.podium[0].driver}
              </div>
              <div className="label text-black opacity-80">
                {race.podium[0].team}
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

// ---------------------------------------------------------------------------
// Car placed at a given fraction (0..1) along the track path.
// ---------------------------------------------------------------------------
const CarOnTrack = ({ pct, color, label, leader, dim }) => {
  // Ref to the invisible path we measure
  const [pt, setPt] = useState({ x: 0, y: 0 });
  const pathRef = useRef(null);
  useEffect(() => {
    const el = pathRef.current;
    if (!el) return;
    const len = el.getTotalLength();
    const p = el.getPointAtLength((1 - pct) * len);
    setPt({ x: p.x, y: p.y });
  }, [pct]);
  return (
    <>
      <path
        ref={pathRef}
        d={TRACK_PATH}
        fill="none"
        stroke="transparent"
        pointerEvents="none"
      />
      <g
        transform={`translate(${pt.x}, ${pt.y})`}
        style={{ transition: "transform 0.32s linear" }}
      >
        <TrackDot pct={pct} color={color} label={label} dim={dim} glow={leader} />
      </g>
    </>
  );
};

// ---------------------------------------------------------------------------
// Single feed row
// ---------------------------------------------------------------------------
const KIND_META = {
  flag: { color: "#F2F2F2", tag: "// FORMAÇÃO" },
  green: { color: "#00FF66", tag: "// LARGADA" },
  overtake: { color: "#E4FF00", tag: "// ULTRAPASSAGEM" },
  dnf: { color: "#FF3B30", tag: "// DNF" },
  sc: { color: "#FF9E00", tag: "// SAFETY CAR" },
  pit: { color: "#00F0FF", tag: "// PIT" },
  fast: { color: "#B0E000", tag: "// VOLTA RÁPIDA" },
  chequered: { color: "#E4FF00", tag: "// BANDEIRADA" },
};

const FeedItem = ({ f }) => {
  const meta = KIND_META[f.kind] || { color: "#888", tag: "// EVENTO" };
  return (
    <div
      className="border-l-2 pl-2 py-1"
      style={{ borderColor: meta.color }}
    >
      <div
        className="text-[9px] tracking-[0.22em] uppercase font-bold"
        style={{ color: meta.color }}
      >
        {meta.tag}
      </div>
      <div className="text-xs text-neutral-200 leading-snug">{f.text}</div>
    </div>
  );
};

export default LiveRaceOverlay;
