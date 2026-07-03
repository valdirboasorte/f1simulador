import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchSeason, createSimulation } from "../lib/api";
import { Header } from "../components/Layout";

const SeasonPage = () => {
  const { year } = useParams();
  const navigate = useNavigate();
  const [season, setSeason] = useState(null);
  const [starting, setStarting] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchSeason(year).then(setSeason).catch(() => setError("Temporada não encontrada"));
  }, [year]);

  const onStart = async () => {
    setStarting(true);
    try {
      const sim = await createSimulation(parseInt(year, 10));
      navigate(`/simulacao/${sim.id}`);
    } catch (e) {
      setError("Falha ao criar simulação. Tente novamente.");
      setStarting(false);
    }
  };

  if (error) {
    return (
      <div>
        <Header />
        <div className="max-w-2xl mx-auto p-10 text-center">
          <div className="label mb-3 text-[#FF3B30]">// ERRO</div>
          <div className="font-head text-2xl">{error}</div>
          <Link to="/" className="text-[#E4FF00] text-sm tracking-[0.22em] uppercase font-bold mt-6 inline-block">
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
            <div className="font-mono-num text-[#E4FF00] text-sm mt-6 mb-4">// TEMPORADA</div>
            <h1
              className="font-head font-black uppercase text-6xl sm:text-7xl lg:text-8xl leading-none tracking-tighter"
              data-testid="season-year"
            >
              {season.year}
            </h1>
            <div className="mt-8 flex flex-wrap gap-8 text-sm">
              <div>
                <div className="label mb-1">Campeão histórico</div>
                <div className="font-head font-bold text-lg tracking-tight" data-testid="real-champion">
                  {season.champion}
                </div>
                <div className="text-neutral-500 text-xs">{season.champion_team}</div>
              </div>
              <div>
                <div className="label mb-1">Construtores</div>
                <div className="font-head font-bold text-lg tracking-tight">{season.constructors_champion}</div>
              </div>
              <div>
                <div className="label mb-1">Etapas</div>
                <div className="font-mono-num text-lg">{season.num_races}</div>
              </div>
            </div>
          </div>
          <div className="md:col-span-4 flex flex-col justify-end">
            <button
              onClick={onStart}
              disabled={starting}
              data-testid="start-simulation-button"
              className="w-full bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-sm py-6 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors border-2 border-transparent focus:border-white outline-none"
            >
              {starting ? "Preparando..." : "Iniciar Temporada →"}
            </button>
            <p className="text-neutral-500 text-xs mt-3 text-center">
              Você vai rodar corrida por corrida, ao seu ritmo.
            </p>
          </div>
        </div>
      </section>

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
            <div key={i} className="bg-[#0A0A0A] p-5 hover:bg-[#141414] transition-colors" data-testid={`driver-${i}`}>
              <div className="flex items-baseline justify-between mb-2">
                <span className="font-mono-num text-neutral-600 text-xs">#{String(i + 1).padStart(2, "0")}</span>
                <span className="font-mono-num text-[#E4FF00] font-bold text-lg">{d.rating}</span>
              </div>
              <div className="font-head font-bold text-base uppercase tracking-tight leading-tight">{d.name}</div>
              <div className="text-neutral-500 text-xs mt-1">{d.team}</div>
              <div className="mt-3 h-1 bg-[#1F1F1F] overflow-hidden">
                <div className="h-full bg-[#E4FF00]" style={{ width: `${d.rating}%` }} />
              </div>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
};

export default SeasonPage;
