import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  fetchSimulation,
  runNextRace,
  finishSimulation,
  commitSeason,
} from "../lib/api";
import { Header } from "../components/Layout";

const RaceCard = ({ race, isLatest, pointsScheme }) => {
  const [expanded, setExpanded] = useState(isLatest);
  const news = race.news;
  const snap = race.standings_snapshot || { drivers: [], constructors: [] };

  return (
    <article
      className={`bg-[#0A0A0A] border ${isLatest ? "border-[#E4FF00]" : "border-[#262626]"} p-6`}
      data-testid={`race-${race.round}`}
    >
      {/* Header */}
      <div className="flex flex-wrap items-baseline justify-between gap-2 mb-4">
        <div className="flex items-baseline gap-3">
          <span className="font-mono-num text-[#E4FF00] font-bold text-lg">
            R{String(race.round).padStart(2, "0")}
          </span>
          <span className="font-head font-black uppercase text-xl tracking-tight">
            {race.circuit}
          </span>
        </div>
        {isLatest && (
          <span className="label text-[#E4FF00]">// ETAPA ATUAL</span>
        )}
      </div>

      {/* News */}
      {news ? (
        <div className="mb-6 border-l-2 border-[#E4FF00] pl-4 bg-[#141414] p-4" data-testid={`race-news-${race.round}`}>
          <div className="label text-[#E4FF00] mb-2">{news.tag || "CORRIDA"}</div>
          <h4 className="font-head font-black uppercase text-lg tracking-tight leading-tight mb-2">
            {news.title}
          </h4>
          {news.subtitle && (
            <div className="text-neutral-400 text-xs mb-3 italic">{news.subtitle}</div>
          )}
          {news.body && (
            <div className="text-neutral-300 text-sm leading-relaxed whitespace-pre-line">
              {news.body}
            </div>
          )}
        </div>
      ) : (
        <div className="mb-6 border-l-2 border-neutral-700 pl-4 text-neutral-500 text-xs italic">
          Manchete indisponível para esta corrida.
        </div>
      )}

      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left label text-neutral-400 hover:text-white mb-3 flex items-center justify-between"
        data-testid={`race-toggle-${race.round}`}
      >
        <span>{expanded ? "▾ Fechar detalhes" : "▸ Ver resultado + classificação"}</span>
      </button>

      {expanded && (
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-6">
          {/* Full race results */}
          <div>
            <div className="label text-neutral-500 mb-2">RESULTADO DA CORRIDA</div>
            <div className="border border-[#262626]" data-testid={`race-results-${race.round}`}>
              <div className="grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] label bg-[#141414]">
                <div className="col-span-1 text-right">Pos</div>
                <div className="col-span-6">Piloto</div>
                <div className="col-span-3">Equipe</div>
                <div className="col-span-2 text-right">Pts</div>
              </div>
              {race.results.map((r, i) => (
                <div
                  key={i}
                  className={`grid grid-cols-12 gap-2 px-3 py-1.5 border-b border-[#262626] items-center text-xs ${
                    r.dnf ? "text-neutral-600" : i === 0 ? "text-[#E4FF00]" : ""
                  }`}
                >
                  <div className="col-span-1 text-right font-mono-num">
                    {r.dnf ? "DNF" : String(r.position).padStart(2, "0")}
                  </div>
                  <div className="col-span-6 font-head font-bold uppercase tracking-tight">
                    {r.driver}
                  </div>
                  <div className="col-span-3 text-neutral-500">{r.team}</div>
                  <div className="col-span-2 text-right font-mono-num font-bold">
                    {r.points || "—"}
                  </div>
                </div>
              ))}
            </div>
            <div className="mt-2 label text-neutral-600">
              Pontos: {pointsScheme.join("-")}
            </div>
          </div>

          {/* Live standings snapshot at this moment */}
          <div>
            <div className="label text-neutral-500 mb-2">
              CLASSIFICAÇÃO APÓS R{String(race.round).padStart(2, "0")}
            </div>
            <div className="border border-[#262626] mb-3" data-testid={`race-snapshot-drivers-${race.round}`}>
              <div className="grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] label bg-[#141414]">
                <div className="col-span-1 text-right">#</div>
                <div className="col-span-7">Piloto</div>
                <div className="col-span-2 text-right">V</div>
                <div className="col-span-2 text-right">Pts</div>
              </div>
              {snap.drivers.map((d, i) => (
                <div
                  key={d.driver}
                  className={`grid grid-cols-12 gap-2 px-3 py-1.5 border-b border-[#262626] items-center text-xs ${
                    i === 0 ? "text-[#E4FF00]" : ""
                  }`}
                >
                  <div className="col-span-1 text-right font-mono-num">
                    {String(i + 1).padStart(2, "0")}
                  </div>
                  <div className="col-span-7 font-head font-bold uppercase tracking-tight">
                    {d.driver}
                  </div>
                  <div className="col-span-2 text-right font-mono-num">{d.wins}</div>
                  <div className="col-span-2 text-right font-mono-num font-bold">
                    {d.points}
                  </div>
                </div>
              ))}
            </div>
            <div className="border border-[#262626]" data-testid={`race-snapshot-constructors-${race.round}`}>
              <div className="grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] label bg-[#141414]">
                <div className="col-span-1 text-right">#</div>
                <div className="col-span-9">Equipe</div>
                <div className="col-span-2 text-right">Pts</div>
              </div>
              {snap.constructors.map((c, i) => (
                <div
                  key={c.team}
                  className={`grid grid-cols-12 gap-2 px-3 py-1.5 border-b border-[#262626] items-center text-xs ${
                    i === 0 ? "text-[#E4FF00]" : ""
                  }`}
                >
                  <div className="col-span-1 text-right font-mono-num">
                    {String(i + 1).padStart(2, "0")}
                  </div>
                  <div className="col-span-9 font-head font-bold uppercase tracking-tight">
                    {c.team}
                  </div>
                  <div className="col-span-2 text-right font-mono-num font-bold">
                    {c.points}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </article>
  );
};

const SimulationPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [latestRound, setLatestRound] = useState(null);
  const [committing, setCommitting] = useState(false);
  const [committed, setCommitted] = useState(false);

  useEffect(() => {
    fetchSimulation(id)
      .then((d) => setData(d))
      .catch(() => setError("Simulação não encontrada"));
  }, [id]);

  const [liveRace, setLiveRace] = useState(null);
  const [liveEvents, setLiveEvents] = useState([]);

  const onNext = async () => {
    if (!data || busy) return;
    setBusy(true);
    setLiveEvents(["> Green flag! Largada em " + (data.circuits[data.current_race] || "")]);
    setLiveRace(true);
    try {
      const upd = await runNextRace(id);
      const race = upd.races[upd.races.length - 1];
      const evts = [];
      race.results.slice(0, 5).forEach((r, i) => {
        evts.push(`> Volta ${20 + i * 8}: ${r.driver} em P${r.position || "DNF"}`);
      });
      const dnfs = race.results.filter((r) => r.dnf);
      dnfs.forEach((r) => evts.push(`> DNF: ${r.driver} abandona`));
      evts.push(`> BANDEIRADA! Vencedor: ${race.podium[0]?.driver || "-"}`);
      for (let i = 0; i < evts.length; i++) {
        await new Promise((res) => setTimeout(res, 700));
        setLiveEvents((prev) => [...prev, evts[i]]);
      }
      await new Promise((res) => setTimeout(res, 900));
      setData(upd);
      setLatestRound(upd.current_race);
      setLiveRace(false);
    } finally {
      setBusy(false);
    }
  };

  const onFinishAll = async () => {
    if (!data || busy) return;
    setBusy(true);
    try {
      const upd = await finishSimulation(id, false);
      setData(upd);
      setLatestRound(upd.current_race);
    } finally {
      setBusy(false);
    }
  };

  const onFinishFast = async () => {
    if (!data || busy) return;
    setBusy(true);
    try {
      const upd = await finishSimulation(id, true);
      setData(upd);
      setLatestRound(upd.current_race);
    } finally {
      setBusy(false);
    }
  };

  const onCommit = async () => {
    if (!data?.reality_id || committing) return;
    setCommitting(true);
    try {
      await commitSeason(data.reality_id, id);
      setCommitted(true);
      setTimeout(() => navigate(`/realidade/${data.reality_id}`), 700);
    } catch (e) {
      setCommitting(false);
    }
  };

  if (error) {
    return (
      <div>
        <Header />
        <div className="p-10 text-center">
          <div className="label mb-3 text-[#FF3B30]">// ERRO</div>
          <div className="font-head text-2xl">{error}</div>
          <Link to="/" className="text-[#E4FF00] mt-6 inline-block label">
            ← Voltar
          </Link>
        </div>
      </div>
    );
  }
  if (!data) {
    return (
      <div>
        <Header />
        <div className="p-10 text-neutral-500 font-mono-num">Carregando simulação...</div>
      </div>
    );
  }

  const s = data.summary;
  const progress = (data.current_race / data.total_races) * 100;
  const nextCircuit = !data.finished ? data.circuits[data.current_race] : null;
  const nextRoundNum = data.current_race + 1;

  return (
    <div>
      <Header />

      {/* Command panel */}
      <section className="border-b border-[#262626] bg-[#0A0A0A] sticky top-16 z-20 backdrop-blur-xl bg-black/80">
        <div className="max-w-[1400px] mx-auto px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            <div className="md:col-span-3">
              <Link
                to={`/temporadas/${data.year}`}
                className="label text-neutral-500 hover:text-[#E4FF00]"
                data-testid="back-season"
              >
                ← {data.year}
              </Link>
              <div className="font-mono-num text-3xl font-bold mt-2" data-testid="progress-counter">
                {String(data.current_race).padStart(2, "0")}
                <span className="text-neutral-600">/{data.total_races}</span>
              </div>
              <div className="label mt-1">Etapas rodadas</div>
            </div>
            <div className="md:col-span-5">
              <div className="h-2 bg-[#1F1F1F] overflow-hidden mb-2">
                <div
                  className="h-full bg-[#E4FF00] transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
              {!data.finished ? (
                <div className="text-sm">
                  <span className="label text-[#E4FF00]">Próxima:</span>
                  <span
                    className="ml-2 font-head font-bold uppercase tracking-tight"
                    data-testid="next-race-circuit"
                  >
                    R{String(nextRoundNum).padStart(2, "0")} · {nextCircuit}
                  </span>
                </div>
              ) : (
                <div className="label text-[#00FF66]" data-testid="season-finished-label">
                  ✓ Temporada encerrada
                </div>
              )}
            </div>
            <div className="md:col-span-4 flex flex-col sm:flex-row gap-2">
              {!data.finished ? (
                <>
                  <button
                    onClick={onNext}
                    disabled={busy}
                    data-testid="next-race-button"
                    className="flex-1 bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs py-4 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors"
                  >
                    {busy ? "Rodando + IA..." : "Simular Próxima →"}
                  </button>
                  <button
                    onClick={onFinishFast}
                    disabled={busy}
                    data-testid="finish-all-button"
                    className="flex-1 border border-[#00F0FF] text-[#00F0FF] font-bold uppercase tracking-[0.22em] text-xs py-4 hover:bg-[#00F0FF] hover:text-black disabled:opacity-50 transition-colors"
                  >
                    ⚡ Simular Rápido
                  </button>
                </>
              ) : (
                <div className="w-full text-center text-[#00FF66] label py-4">
                  ✓ Todas as manchetes publicadas
                </div>
              )}
            </div>
          </div>
          {data.finished && data.reality_id && (
            <div className="mt-4 border-t border-[#262626] pt-4 flex flex-wrap items-center justify-between gap-3">
              <div className="label text-neutral-400">
                Esta temporada faz parte de uma <span className="text-[#E4FF00]">Minha Realidade</span>. Registre para avançar o ano.
              </div>
              <button
                onClick={onCommit}
                disabled={committing || committed}
                data-testid="commit-reality-button"
                className="bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs px-6 py-3 hover:bg-[#C6DB00] disabled:opacity-50"
              >
                {committed ? "✓ Registrado" : committing ? "Salvando..." : "Registrar & Avançar →"}
              </button>
            </div>
          )}
        </div>
      </section>

      {/* Verdict when finished */}
      {data.finished && s.champion && (
        <section className="border-b border-[#262626]">
          <div className="max-w-[1400px] mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-12 gap-10 items-end">
            <div className="md:col-span-8">
              <div className="label text-[#E4FF00] mb-3">// VEREDITO</div>
              <h1
                className="font-head font-black uppercase text-4xl sm:text-6xl lg:text-7xl tracking-tighter leading-[0.9]"
                data-testid="sim-champion-name"
              >
                {s.champion.driver}
              </h1>
              <div className="mt-4 text-xl text-neutral-300">
                campeão de <span className="text-[#E4FF00]">{data.year}</span> pela{" "}
                <span className="font-bold">{s.champion.team}</span>
              </div>
              {s.upset ? (
                <div
                  className="mt-6 inline-block border border-[#FF3B30] text-[#FF3B30] px-3 py-1 label"
                  data-testid="upset-badge"
                >
                  REVIRAVOLTA · Histórico: {s.real_champion.driver}
                </div>
              ) : (
                <div className="mt-6 inline-block border border-[#00FF66] text-[#00FF66] px-3 py-1 label">
                  CONFIRMADO · Coincide com a história
                </div>
              )}
            </div>
            <div className="md:col-span-4 border border-[#262626] p-6">
              <div className="label mb-2">Construtores</div>
              <div className="font-head font-bold text-2xl uppercase tracking-tight text-[#E4FF00]">
                {s.constructor_champion?.team}
              </div>
              <div className="mt-1 font-mono-num text-neutral-400 text-sm">
                {s.constructor_champion?.points} pts · histórico: {s.real_constructor_champion}
              </div>
            </div>
          </div>
        </section>
      )}

      {/* Race feed */}
      <section className="max-w-[1400px] mx-auto px-6 py-16">
        <div className="label text-[#E4FF00] mb-3">// FEED DA TEMPORADA</div>
        <h2 className="font-head font-black uppercase text-3xl sm:text-4xl tracking-tighter mb-8">
          Corrida a corrida
        </h2>
        {data.races.length === 0 ? (
          <div className="border border-dashed border-[#262626] p-10 text-center">
            <div className="label text-neutral-500 mb-3">// AGUARDANDO PRIMEIRA CORRIDA</div>
            <p className="text-neutral-400 text-sm">
              Clique em{" "}
              <span className="text-[#E4FF00] font-bold">&quot;Simular Próxima →&quot;</span> acima
              para rodar a etapa {nextRoundNum} em {nextCircuit}. A cada corrida uma manchete de IA é gerada automaticamente.
            </p>
          </div>
        ) : (
          <div className="space-y-6" data-testid="races-feed">
            {[...data.races].reverse().map((r) => (
              <RaceCard
                key={r.round}
                race={r}
                isLatest={r.round === latestRound || r.round === data.current_race}
                pointsScheme={data.points_scheme}
              />
            ))}
          </div>
        )}
      </section>

      <footer className="border-t border-[#262626] py-10 text-center text-neutral-600 text-xs tracking-[0.22em] uppercase">
        SIM #{data.id?.slice(0, 8).toUpperCase()} · SEED {data.seed}
      </footer>
    </div>
  );
};

export default SimulationPage;
