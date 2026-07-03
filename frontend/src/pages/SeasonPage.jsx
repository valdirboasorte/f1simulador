import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchSeason, runSimulation } from "../lib/api";
import { Header } from "../components/Layout";

const LoaderTerminal = ({ year }) => {
  const [lines, setLines] = useState([]);
  useEffect(() => {
    const tick = [
      "> boot alt-reality engine v2.6...",
      `> loading season ${year} roster ...`,
      "> injecting stochastic noise σ=8.0",
      "> race 1 :: pole position calculated",
      "> race 2 :: dnf roll = 0.031 -> RETIRED",
      "> race 3 :: podium locked",
      "> race 4 :: overtaking simulation ok",
      "> race 5 :: safety car deployed",
      "> race 6 :: constructor points += 43",
      "> race 7 :: championship gap = 12pts",
      "> spawning gemini-3-flash news writer ...",
      "> composing headlines in pt-BR ...",
      "> render alternate history ...",
    ];
    let i = 0;
    const id = setInterval(() => {
      setLines((prev) => [...prev, tick[i % tick.length]]);
      i++;
    }, 220);
    return () => clearInterval(id);
  }, [year]);
  return (
    <div
      className="fixed inset-0 z-50 bg-black/95 flex items-center justify-center p-6"
      data-testid="simulate-loader"
    >
      <div className="w-full max-w-2xl border border-[#262626] bg-[#0A0A0A] p-6">
        <div className="flex items-center justify-between mb-4">
          <div className="label text-[#E4FF00]">// SIMULANDO {year}</div>
          <div className="flex gap-1">
            <span className="w-2 h-2 bg-[#E4FF00] animate-pulse" />
            <span
              className="w-2 h-2 bg-[#00F0FF] animate-pulse"
              style={{ animationDelay: "0.15s" }}
            />
            <span
              className="w-2 h-2 bg-[#FF3B30] animate-pulse"
              style={{ animationDelay: "0.3s" }}
            />
          </div>
        </div>
        <div className="font-mono-num text-xs text-[#00FF66] h-64 overflow-hidden">
          {lines.slice(-12).map((l, i) => (
            <div key={i} className="leading-5">
              {l}
            </div>
          ))}
        </div>
        <div className="mt-4 h-1 bg-[#262626] overflow-hidden">
          <div
            className="h-full bg-[#E4FF00]"
            style={{ width: "100%", animation: "fade-up 1.5s ease-in-out infinite" }}
          />
        </div>
      </div>
    </div>
  );
};

const SeasonPage = () => {
  const { year } = useParams();
  const navigate = useNavigate();
  const [season, setSeason] = useState(null);
  const [simulating, setSimulating] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSeason(year).then(setSeason).catch(() => setError("Temporada não encontrada"));
  }, [year]);

  const onSimulate = async () => {
    setSimulating(true);
    try {
      const result = await runSimulation(parseInt(year, 10));
      navigate(`/simulacao/${result.id}`);
    } catch (e) {
      setError("Falha ao simular. Tente novamente.");
      setSimulating(false);
    }
  };

  if (error) {
    return (
      <div>
        <Header />
        <div className="max-w-2xl mx-auto p-10 text-center">
          <div className="label mb-3 text-[#FF3B30]">// ERRO</div>
          <div className="font-head text-2xl">{error}</div>
          <Link
            to="/"
            className="text-[#E4FF00] text-sm tracking-[0.22em] uppercase font-bold mt-6 inline-block"
          >
            ← Voltar
          </Link>
        </div>
      </div>
    );
  }

  if (!season) {
    return (
      <div>
        <Header />
        <div className="p-10 text-neutral-500 font-mono-num">Carregando...</div>
      </div>
    );
  }

  return (
    <div>
      <Header />
      {simulating && <LoaderTerminal year={year} />}

      <section className="border-b border-[#262626]">
        <div className="max-w-[1400px] mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-12 gap-8">
          <div className="md:col-span-8">
            <Link
              to="/"
              className="label text-neutral-500 hover:text-[#E4FF00] transition-colors"
              data-testid="back-home"
            >
              ← Escolher outra temporada
            </Link>
            <div className="font-mono-num text-[#E4FF00] text-sm mt-6 mb-4">
              // TEMPORADA
            </div>
            <h1
              className="font-head font-black uppercase text-6xl sm:text-7xl lg:text-8xl leading-none tracking-tighter"
              data-testid="season-year"
            >
              {season.year}
            </h1>
            <div className="mt-8 flex flex-wrap gap-8 text-sm">
              <div>
                <div className="label mb-1">Campeão histórico</div>
                <div
                  className="font-head font-bold text-lg tracking-tight"
                  data-testid="real-champion"
                >
                  {season.champion}
                </div>
                <div className="text-neutral-500 text-xs">{season.champion_team}</div>
              </div>
              <div>
                <div className="label mb-1">Construtores</div>
                <div className="font-head font-bold text-lg tracking-tight">
                  {season.constructors_champion}
                </div>
              </div>
              <div>
                <div className="label mb-1">Etapas</div>
                <div className="font-mono-num text-lg">{season.num_races}</div>
              </div>
            </div>
          </div>
          <div className="md:col-span-4 flex flex-col justify-end">
            <button
              onClick={onSimulate}
              disabled={simulating}
              data-testid="simulate-button"
              className="w-full bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-sm py-6 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors border-2 border-transparent focus:border-white outline-none"
            >
              {simulating ? "Simulando..." : "Rodar Simulação →"}
            </button>
            <p className="text-neutral-500 text-xs mt-3 text-center">
              Gera notícias com IA. Pode levar ~15-30s.
            </p>
          </div>
        </div>
      </section>

      {/* Roster */}
      <section className="max-w-[1400px] mx-auto px-6 py-16">
        <div className="label text-[#E4FF00] mb-3">// GRID DA TEMPORADA</div>
        <h2 className="font-head font-black uppercase text-3xl tracking-tighter mb-8">
          Pilotos e ratings
        </h2>
        <div
          className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-px bg-[#262626] border border-[#262626]"
          data-testid="roster-grid"
        >
          {season.drivers.map((d, i) => (
            <div
              key={i}
              className="bg-[#0A0A0A] p-5 hover:bg-[#141414] transition-colors"
              data-testid={`driver-${i}`}
            >
              <div className="flex items-baseline justify-between mb-2">
                <span className="font-mono-num text-neutral-600 text-xs">
                  #{String(i + 1).padStart(2, "0")}
                </span>
                <span className="font-mono-num text-[#E4FF00] font-bold text-lg">
                  {d.rating}
                </span>
              </div>
              <div className="font-head font-bold text-base uppercase tracking-tight leading-tight">
                {d.name}
              </div>
              <div className="text-neutral-500 text-xs mt-1">{d.team}</div>
              <div className="mt-3 h-1 bg-[#1F1F1F] overflow-hidden">
                <div
                  className="h-full bg-[#E4FF00]"
                  style={{ width: `${d.rating}%` }}
                />
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default SeasonPage;
