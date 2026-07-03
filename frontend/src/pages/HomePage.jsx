import { useEffect, useMemo, useState } from "react";
import { Link } from "react-router-dom";
import { fetchSeasons } from "../lib/api";
import { Header, Hero } from "../components/Layout";

const DECADES = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2020];

const HomePage = () => {
  const [seasons, setSeasons] = useState([]);
  const [decade, setDecade] = useState(2020);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchSeasons()
      .then(setSeasons)
      .finally(() => setLoading(false));
  }, []);

  const filtered = useMemo(
    () => seasons.filter((s) => s.year >= decade && s.year < decade + 10),
    [seasons, decade],
  );

  const scrollToPicker = () => {
    document
      .getElementById("season-picker")
      ?.scrollIntoView({ behavior: "smooth", block: "start" });
  };

  return (
    <div>
      <Header />
      <Hero onCta={scrollToPicker} />

      {/* Minha Realidade promo */}
      <section className="border-b border-[#262626] bg-[#0A0A0A]">
        <div className="max-w-[1400px] mx-auto px-6 py-12 flex flex-wrap items-center justify-between gap-6">
          <div>
            <div className="label text-[#E4FF00] mb-2">// NOVO MODO</div>
            <h3 className="font-head font-black uppercase text-2xl sm:text-3xl tracking-tighter">
              Modo <span className="text-[#E4FF00]">Minha Realidade</span> — 1950 → 2025
            </h3>
            <p className="text-neutral-400 text-sm mt-2 max-w-xl">
              Simule cronologicamente cada temporada e acumule vitórias, pódios e títulos por piloto/equipe. Sua timeline alternativa persistente.
            </p>
          </div>
          <Link
            to="/realidade"
            data-testid="cta-reality"
            className="border-2 border-[#E4FF00] text-[#E4FF00] font-black uppercase tracking-[0.22em] text-xs px-8 py-4 hover:bg-[#E4FF00] hover:text-black transition-colors"
          >
            Iniciar Timeline →
          </Link>
        </div>
      </section>

      <section
        id="season-picker"
        className="max-w-[1400px] mx-auto px-6 py-20"
        data-testid="season-picker-section"
      >
        <div className="grid grid-cols-1 md:grid-cols-12 gap-8 mb-10">
          <div className="md:col-span-5">
            <div className="label mb-4 text-[#E4FF00]">// PASSO 01</div>
            <h2 className="font-head font-black uppercase text-3xl sm:text-4xl lg:text-5xl tracking-tighter leading-[0.95]">
              Escolha uma<br />temporada
            </h2>
          </div>
          <div className="md:col-span-7 flex md:justify-end items-end">
            <p className="text-neutral-400 text-sm max-w-md">
              Cada temporada tem seu próprio grid de pilotos, equipes e
              circuitos daquela era. A simulação usa ratings históricos +
              aleatoriedade.
            </p>
          </div>
        </div>

        {/* Decade selector */}
        <div className="flex flex-wrap gap-2 mb-8" data-testid="decade-selector">
          {DECADES.map((d) => (
            <button
              key={d}
              onClick={() => setDecade(d)}
              data-testid={`decade-${d}`}
              className={`font-mono-num text-sm px-5 py-3 border transition-colors ${
                decade === d
                  ? "bg-[#E4FF00] text-black border-[#E4FF00] font-bold"
                  : "text-neutral-400 border-[#262626] hover:border-white hover:text-white"
              }`}
            >
              {d}s
            </button>
          ))}
        </div>

        {loading ? (
          <div className="text-neutral-500 font-mono-num" data-testid="seasons-loading">
            Carregando temporadas...
          </div>
        ) : (
          <div
            className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-px bg-[#262626] border border-[#262626]"
            data-testid="seasons-grid"
          >
            {filtered.map((s) => (
              <Link
                key={s.year}
                to={`/temporadas/${s.year}`}
                data-testid={`season-card-${s.year}`}
                className="group bg-[#0A0A0A] hover:bg-[#141414] p-6 transition-colors relative"
              >
                <div className="font-mono-num text-4xl font-bold tracking-tighter text-white group-hover:text-[#E4FF00] transition-colors">
                  {s.year}
                </div>
                <div className="mt-3 label text-neutral-500">Campeão real</div>
                <div className="mt-1 font-head font-bold text-base uppercase leading-tight tracking-tight">
                  {s.champion}
                </div>
                <div className="text-xs text-neutral-500 mt-1">
                  {s.champion_team}
                </div>
                <div className="mt-4 pt-4 border-t border-[#262626] flex items-center justify-between text-xs">
                  <span className="font-mono-num text-neutral-500">
                    {s.num_races} GPs
                  </span>
                  <span className="text-[#E4FF00] opacity-0 group-hover:opacity-100 transition-opacity tracking-[0.22em] uppercase font-bold">
                    Simular →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>

      {/* How it works */}
      <section className="border-t border-[#262626] bg-[#0A0A0A]">
        <div className="max-w-[1400px] mx-auto px-6 py-24 grid grid-cols-1 md:grid-cols-3 gap-px bg-[#262626]">
          {[
            {
              n: "01",
              t: "Ratings reais",
              d: "Cada piloto tem rating baseado no seu desempenho histórico real naquela temporada específica.",
            },
            {
              n: "02",
              t: "Motor estocástico",
              d: "Corridas rodam com ratings + ruído gaussiano + chance de abandono. Nem sempre o favorito ganha.",
            },
            {
              n: "03",
              t: "Notícias de IA",
              d: "Manchetes e reportagens em português geradas por Gemini 3 Flash a partir do resultado simulado.",
            },
          ].map((x) => (
            <div key={x.n} className="bg-[#0A0A0A] p-8 md:p-10">
              <div className="font-mono-num text-[#E4FF00] text-sm mb-6">
                // {x.n}
              </div>
              <h3 className="font-head font-black uppercase text-2xl tracking-tight mb-3">
                {x.t}
              </h3>
              <p className="text-neutral-400 text-sm leading-relaxed">{x.d}</p>
            </div>
          ))}
        </div>
      </section>

      <footer className="border-t border-[#262626] py-10 text-center text-neutral-600 text-xs tracking-[0.22em] uppercase">
        GRID/ALT · Simulador Não-Oficial · 1950—2025
      </footer>
    </div>
  );
};

export default HomePage;
