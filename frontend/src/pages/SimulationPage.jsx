import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { fetchSimulation, runSimulation } from "../lib/api";
import { Header } from "../components/Layout";

const NEWS_IMGS = [
  "https://images.unsplash.com/photo-1614949194403-9602bdc14a3a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzNDR8MHwxfHNlYXJjaHwzfHxmMSUyMHJhY2UlMjBjYXIlMjB0cmFjayUyMGRhcmt8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1742744652734-d5ec6598b5da?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzNDR8MHwxfHNlYXJjaHwxfHxmMSUyMHJhY2UlMjBjYXIlMjB0cmFjayUyMGRhcmt8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1552255472-3330e5928013?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwyfHxyYWNpbmclMjBkcml2ZXIlMjBoZWxtZXR8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1533573271545-c1604421c980?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwzfHxyYWNpbmclMjBkcml2ZXIlMjBoZWxtZXR8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
];

const Section = ({ label, title, children, testid }) => (
  <section className="max-w-[1400px] mx-auto px-6 py-16 border-b border-[#262626]" data-testid={testid}>
    <div className="label text-[#E4FF00] mb-3">// {label}</div>
    <h2 className="font-head font-black uppercase text-3xl sm:text-4xl tracking-tighter mb-10">
      {title}
    </h2>
    {children}
  </section>
);

const SimulationPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);
  const [rerunning, setRerunning] = useState(false);

  useEffect(() => {
    fetchSimulation(id).then(setData).catch(() => setError("Simulação não encontrada"));
  }, [id]);

  const onReSimulate = async () => {
    if (!data) return;
    setRerunning(true);
    try {
      const result = await runSimulation(data.year);
      navigate(`/simulacao/${result.id}`);
      setTimeout(() => window.location.reload(), 100);
    } catch (e) {
      setRerunning(false);
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

  const sim = data.simulation;
  const s = sim.summary;
  const news = data.news || [];

  return (
    <div>
      <Header />

      {/* Hero verdict */}
      <section className="border-b border-[#262626] bg-[#0A0A0A]">
        <div className="max-w-[1400px] mx-auto px-6 py-16 grid grid-cols-1 md:grid-cols-12 gap-10">
          <div className="md:col-span-7">
            <Link
              to={`/temporadas/${sim.year}`}
              className="label text-neutral-500 hover:text-[#E4FF00] transition-colors"
              data-testid="back-season"
            >
              ← {sim.year}
            </Link>
            <div className="font-mono-num text-[#E4FF00] text-sm mt-6 mb-3">
              // VEREDITO DA REALIDADE ALTERNATIVA
            </div>
            <h1
              className="font-head font-black uppercase text-4xl sm:text-6xl lg:text-7xl tracking-tighter leading-[0.9]"
              data-testid="sim-champion-name"
            >
              {s.champion.driver}
            </h1>
            <div className="mt-4 text-xl text-neutral-300">
              é campeão de <span className="text-[#E4FF00]">{sim.year}</span> pela{" "}
              <span className="font-bold">{s.champion.team}</span>
            </div>
            {s.upset && (
              <div className="mt-6 inline-block border border-[#FF3B30] text-[#FF3B30] px-3 py-1 label" data-testid="upset-badge">
                REVIRAVOLTA · Histórico: {s.real_champion.driver}
              </div>
            )}
            {!s.upset && (
              <div className="mt-6 inline-block border border-[#00FF66] text-[#00FF66] px-3 py-1 label">
                CONFIRMADO · Coincide com a história
              </div>
            )}
          </div>
          <div className="md:col-span-5 flex flex-col gap-4">
            <div className="border border-[#262626] p-6">
              <div className="label mb-2">Vice</div>
              <div className="font-head font-bold text-xl uppercase tracking-tight">
                {s.runner_up?.driver}
              </div>
              <div className="text-neutral-500 text-xs">{s.runner_up?.team}</div>
              <div className="mt-3 font-mono-num text-neutral-400 text-sm">
                {s.runner_up?.points} pts · {s.runner_up?.wins} vitórias
              </div>
            </div>
            <div className="border border-[#262626] p-6 bg-[#141414]">
              <div className="label mb-2">Construtores simulado</div>
              <div className="font-head font-bold text-xl uppercase tracking-tight text-[#E4FF00]">
                {s.constructor_champion?.team}
              </div>
              <div className="mt-2 font-mono-num text-neutral-400 text-sm">
                {s.constructor_champion?.points} pts · histórico: {s.real_constructor_champion}
              </div>
            </div>
            <button
              onClick={onReSimulate}
              disabled={rerunning}
              data-testid="resimulate-button"
              className="bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs py-4 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors"
            >
              {rerunning ? "Rodando..." : "↻ Simular Novamente"}
            </button>
          </div>
        </div>
      </section>

      {/* News */}
      {news.length > 0 && (
        <Section label="MANCHETES DA REALIDADE ALTERNATIVA" title="Cobertura Editorial" testid="news-section">
          <div className="grid grid-cols-1 md:grid-cols-6 gap-px bg-[#262626] border border-[#262626]">
            {news.map((n, i) => {
              const isBig = i === 0;
              return (
                <article
                  key={i}
                  data-testid={`news-card-${i}`}
                  className={`bg-[#0A0A0A] p-6 md:p-8 relative overflow-hidden group hover:bg-[#141414] transition-all ${
                    isBig ? "md:col-span-4 md:row-span-2 min-h-[420px]" : "md:col-span-2 min-h-[210px]"
                  }`}
                >
                  <div
                    className={`absolute inset-0 bg-cover bg-center opacity-30 group-hover:opacity-40 transition-opacity`}
                    style={{ backgroundImage: `url(${NEWS_IMGS[i % NEWS_IMGS.length]})` }}
                  />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-black/40" />
                  <div className="relative flex flex-col h-full justify-end">
                    <div className="label text-[#E4FF00] mb-3">{n.tag || "F1"}</div>
                    <h3 className={`font-head font-black uppercase tracking-tighter leading-[0.95] mb-3 ${isBig ? "text-3xl sm:text-4xl lg:text-5xl" : "text-xl sm:text-2xl"}`}>
                      {n.title}
                    </h3>
                    {n.subtitle && (
                      <div className="text-neutral-300 text-sm mb-3">{n.subtitle}</div>
                    )}
                    {isBig && n.body && (
                      <div className="text-neutral-400 text-sm leading-relaxed whitespace-pre-line max-w-2xl">
                        {n.body}
                      </div>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        </Section>
      )}

      {/* Drivers standings */}
      <Section label="CLASSIFICAÇÃO FINAL" title="Pilotos" testid="drivers-standings-section">
        <div className="border border-[#262626]" data-testid="drivers-table">
          <div className="grid grid-cols-12 gap-4 px-4 py-3 border-b border-[#262626] label bg-[#141414]">
            <div className="col-span-1 text-right">Pos</div>
            <div className="col-span-5">Piloto</div>
            <div className="col-span-3">Equipe</div>
            <div className="col-span-1 text-right">V</div>
            <div className="col-span-1 text-right">Pod</div>
            <div className="col-span-1 text-right">Pts</div>
          </div>
          {sim.driver_standings.map((d, i) => {
            const isChamp = i === 0;
            return (
              <div
                key={d.driver}
                data-testid={`driver-row-${i}`}
                className={`grid grid-cols-12 gap-4 px-4 py-3 border-b border-[#262626] items-center ${
                  isChamp ? "bg-[#E4FF00]/10 text-[#E4FF00]" : "hover:bg-[#141414]"
                }`}
              >
                <div className="col-span-1 text-right font-mono-num text-sm">
                  {String(i + 1).padStart(2, "0")}
                </div>
                <div className="col-span-5 font-head font-bold uppercase text-sm tracking-tight">
                  {d.driver}
                </div>
                <div className="col-span-3 text-sm text-neutral-400">{d.team}</div>
                <div className="col-span-1 text-right font-mono-num text-sm">{d.wins}</div>
                <div className="col-span-1 text-right font-mono-num text-sm">{d.podiums}</div>
                <div className="col-span-1 text-right font-mono-num font-bold text-sm">{d.points}</div>
              </div>
            );
          })}
        </div>
      </Section>

      {/* Constructors */}
      <Section label="CLASSIFICAÇÃO" title="Construtores" testid="constructors-section">
        <div className="border border-[#262626]" data-testid="constructors-table">
          <div className="grid grid-cols-12 gap-4 px-4 py-3 border-b border-[#262626] label bg-[#141414]">
            <div className="col-span-1 text-right">Pos</div>
            <div className="col-span-9">Equipe</div>
            <div className="col-span-2 text-right">Pontos</div>
          </div>
          {sim.constructor_standings.map((c, i) => (
            <div
              key={c.team}
              className={`grid grid-cols-12 gap-4 px-4 py-3 border-b border-[#262626] ${
                i === 0 ? "bg-[#E4FF00]/10 text-[#E4FF00]" : "hover:bg-[#141414]"
              }`}
              data-testid={`constructor-row-${i}`}
            >
              <div className="col-span-1 text-right font-mono-num text-sm">
                {String(i + 1).padStart(2, "0")}
              </div>
              <div className="col-span-9 font-head font-bold uppercase text-sm tracking-tight">
                {c.team}
              </div>
              <div className="col-span-2 text-right font-mono-num font-bold text-sm">
                {c.points}
              </div>
            </div>
          ))}
        </div>
      </Section>

      {/* Races timeline */}
      <Section label="CALENDÁRIO SIMULADO" title="Corrida a corrida" testid="races-section">
        <div className="relative pl-8 border-l-2 border-[#262626]" data-testid="races-timeline">
          {sim.races.map((r) => (
            <div key={r.round} className="mb-8 relative">
              <div className="absolute -left-[41px] top-2 w-4 h-4 bg-[#00F0FF]" />
              <div className="flex flex-wrap items-baseline gap-4 mb-3">
                <span className="font-mono-num text-[#E4FF00] text-sm">
                  R{String(r.round).padStart(2, "0")}
                </span>
                <span className="font-head font-black uppercase text-xl tracking-tight">
                  {r.circuit}
                </span>
              </div>
              <div className="grid grid-cols-1 sm:grid-cols-3 gap-px bg-[#262626] border border-[#262626] max-w-3xl">
                {r.podium.map((p) => (
                  <div key={p.position} className="bg-[#0A0A0A] p-4">
                    <div className="label text-neutral-500 mb-1">
                      {p.position === 1 ? "🏆 P1" : `P${p.position}`}
                    </div>
                    <div className="font-head font-bold text-base uppercase tracking-tight leading-tight">
                      {p.driver}
                    </div>
                    <div className="text-neutral-500 text-xs">{p.team}</div>
                  </div>
                ))}
                {r.podium.length === 0 && (
                  <div className="bg-[#0A0A0A] p-4 text-neutral-500 text-sm col-span-3">
                    Sem pódio registrado
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      </Section>

      <footer className="border-t border-[#262626] py-10 text-center text-neutral-600 text-xs tracking-[0.22em] uppercase">
        SIMULAÇÃO #{data.id?.slice(0, 8).toUpperCase()} · SEED {data.seed}
      </footer>
    </div>
  );
};

export default SimulationPage;
