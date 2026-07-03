import { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";
import {
  fetchSimulation,
  runNextRace,
  finishSimulation,
  generateNews,
} from "../lib/api";
import { Header } from "../components/Layout";

const NEWS_IMGS = [
  "https://images.unsplash.com/photo-1614949194403-9602bdc14a3a?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzNDR8MHwxfHNlYXJjaHwzfHxmMSUyMHJhY2UlMjBjYXIlMjB0cmFjayUyMGRhcmt8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1742744652734-d5ec6598b5da?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzNDR8MHwxfHNlYXJjaHwxfHxmMSUyMHJhY2UlMjBjYXIlMjB0cmFjayUyMGRhcmt8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1552255472-3330e5928013?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwyfHxyYWNpbmclMjBkcml2ZXIlMjBoZWxtZXR8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
  "https://images.unsplash.com/photo-1533573271545-c1604421c980?crop=entropy&cs=srgb&fm=jpg&ixid=M3w3NDQ2NDF8MHwxfHNlYXJjaHwzfHxyYWNpbmclMjBkcml2ZXIlMjBoZWxtZXR8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85",
];

const RaceCard = ({ race, isLatest }) => (
  <div className={`bg-[#0A0A0A] border border-[#262626] p-5 ${isLatest ? "ring-1 ring-[#E4FF00]" : ""}`} data-testid={`race-${race.round}`}>
    <div className="flex items-baseline justify-between mb-3">
      <span className="font-mono-num text-[#E4FF00] text-sm">R{String(race.round).padStart(2, "0")}</span>
      <span className="text-neutral-500 text-xs uppercase tracking-[0.22em]">{race.circuit}</span>
    </div>
    <div className="grid grid-cols-3 gap-px bg-[#262626] border border-[#262626]">
      {race.podium.map((p) => (
        <div key={p.position} className="bg-[#141414] p-3">
          <div className="label text-neutral-500 mb-1">P{p.position}</div>
          <div className="font-head font-bold text-sm uppercase tracking-tight leading-tight">{p.driver}</div>
          <div className="text-neutral-500 text-[10px] mt-0.5">{p.team}</div>
        </div>
      ))}
      {race.podium.length === 0 && (
        <div className="bg-[#141414] p-3 col-span-3 text-neutral-500 text-xs">Sem pódio</div>
      )}
    </div>
  </div>
);

const StandingsCompact = ({ drivers, constructors }) => (
  <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
    <div className="border border-[#262626]" data-testid="standings-drivers">
      <div className="grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] label bg-[#141414]">
        <div className="col-span-1 text-right">#</div>
        <div className="col-span-6">Piloto</div>
        <div className="col-span-3">Equipe</div>
        <div className="col-span-2 text-right">Pts</div>
      </div>
      {drivers.slice(0, 10).map((d, i) => (
        <div
          key={d.driver}
          className={`grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] items-center text-sm ${i === 0 ? "bg-[#E4FF00]/10 text-[#E4FF00]" : ""}`}
          data-testid={`driver-row-${i}`}
        >
          <div className="col-span-1 text-right font-mono-num text-xs">{String(i + 1).padStart(2, "0")}</div>
          <div className="col-span-6 font-head font-bold uppercase tracking-tight text-xs">{d.driver}</div>
          <div className="col-span-3 text-neutral-500 text-xs">{d.team}</div>
          <div className="col-span-2 text-right font-mono-num font-bold text-xs">{d.points}</div>
        </div>
      ))}
    </div>
    <div className="border border-[#262626]" data-testid="standings-constructors">
      <div className="grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] label bg-[#141414]">
        <div className="col-span-1 text-right">#</div>
        <div className="col-span-9">Equipe</div>
        <div className="col-span-2 text-right">Pts</div>
      </div>
      {constructors.slice(0, 10).map((c, i) => (
        <div
          key={c.team}
          className={`grid grid-cols-12 gap-2 px-3 py-2 border-b border-[#262626] items-center text-sm ${i === 0 ? "bg-[#E4FF00]/10 text-[#E4FF00]" : ""}`}
          data-testid={`constructor-row-${i}`}
        >
          <div className="col-span-1 text-right font-mono-num text-xs">{String(i + 1).padStart(2, "0")}</div>
          <div className="col-span-9 font-head font-bold uppercase tracking-tight text-xs">{c.team}</div>
          <div className="col-span-2 text-right font-mono-num font-bold text-xs">{c.points}</div>
        </div>
      ))}
    </div>
  </div>
);

const SimulationPage = () => {
  const { id } = useParams();
  const [data, setData] = useState(null);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState(null);
  const [latestRound, setLatestRound] = useState(null);
  const [generatingNews, setGeneratingNews] = useState(false);

  useEffect(() => {
    fetchSimulation(id).then((d) => setData(d)).catch(() => setError("Simulação não encontrada"));
  }, [id]);

  const onNext = async () => {
    if (!data || busy) return;
    setBusy(true);
    try {
      const upd = await runNextRace(id);
      setData(upd);
      setLatestRound(upd.current_race);
    } finally {
      setBusy(false);
    }
  };

  const onFinishAll = async () => {
    if (!data || busy) return;
    setBusy(true);
    try {
      const upd = await finishSimulation(id);
      setData(upd);
      setLatestRound(upd.current_race);
    } finally {
      setBusy(false);
    }
  };

  const onNews = async () => {
    if (!data || generatingNews) return;
    setGeneratingNews(true);
    try {
      const res = await generateNews(id);
      setData({ ...data, news: res.news });
    } finally {
      setGeneratingNews(false);
    }
  };

  if (error) {
    return (
      <div>
        <Header />
        <div className="p-10 text-center">
          <div className="label mb-3 text-[#FF3B30]">// ERRO</div>
          <div className="font-head text-2xl">{error}</div>
          <Link to="/" className="text-[#E4FF00] mt-6 inline-block label">← Voltar</Link>
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
  const news = data.news || [];

  return (
    <div>
      <Header />

      {/* Command panel */}
      <section className="border-b border-[#262626] bg-[#0A0A0A] sticky top-16 z-20 backdrop-blur-xl bg-black/80">
        <div className="max-w-[1400px] mx-auto px-6 py-6">
          <div className="grid grid-cols-1 md:grid-cols-12 gap-6 items-center">
            <div className="md:col-span-3">
              <Link to={`/temporadas/${data.year}`} className="label text-neutral-500 hover:text-[#E4FF00]" data-testid="back-season">← {data.year}</Link>
              <div className="font-mono-num text-3xl font-bold mt-2" data-testid="progress-counter">
                {String(data.current_race).padStart(2, "0")}<span className="text-neutral-600">/{data.total_races}</span>
              </div>
              <div className="label mt-1">Etapas rodadas</div>
            </div>
            <div className="md:col-span-5">
              <div className="h-2 bg-[#1F1F1F] overflow-hidden mb-2">
                <div className="h-full bg-[#E4FF00] transition-all duration-500" style={{ width: `${progress}%` }} />
              </div>
              {!data.finished ? (
                <div className="text-sm">
                  <span className="label text-[#E4FF00]">Próxima:</span>
                  <span className="ml-2 font-head font-bold uppercase tracking-tight" data-testid="next-race-circuit">
                    R{String(nextRoundNum).padStart(2, "0")} · {nextCircuit}
                  </span>
                </div>
              ) : (
                <div className="label text-[#00FF66]" data-testid="season-finished-label">✓ Temporada encerrada</div>
              )}
            </div>
            <div className="md:col-span-4 flex flex-col sm:flex-row gap-2">
              {!data.finished && (
                <>
                  <button
                    onClick={onNext}
                    disabled={busy}
                    data-testid="next-race-button"
                    className="flex-1 bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs py-4 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors"
                  >
                    {busy ? "..." : "Simular Próxima →"}
                  </button>
                  <button
                    onClick={onFinishAll}
                    disabled={busy}
                    data-testid="finish-all-button"
                    className="flex-1 border border-[#262626] text-white font-bold uppercase tracking-[0.22em] text-xs py-4 hover:border-white disabled:opacity-50 transition-colors"
                  >
                    Rodar Tudo »»
                  </button>
                </>
              )}
              {data.finished && news.length === 0 && (
                <button
                  onClick={onNews}
                  disabled={generatingNews}
                  data-testid="generate-news-button"
                  className="w-full bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs py-4 hover:bg-[#C6DB00] disabled:opacity-50 transition-colors"
                >
                  {generatingNews ? "Gerando manchetes..." : "Gerar Manchetes IA →"}
                </button>
              )}
              {data.finished && news.length > 0 && (
                <div className="w-full text-center text-[#00FF66] label py-4" data-testid="news-ready-label">
                  ✓ Cobertura publicada abaixo
                </div>
              )}
            </div>
          </div>
        </div>
      </section>

      {/* Verdict when finished */}
      {data.finished && s.champion && (
        <section className="border-b border-[#262626]">
          <div className="max-w-[1400px] mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-12 gap-10 items-end">
            <div className="md:col-span-8">
              <div className="label text-[#E4FF00] mb-3">// VEREDITO</div>
              <h1 className="font-head font-black uppercase text-4xl sm:text-6xl lg:text-7xl tracking-tighter leading-[0.9]" data-testid="sim-champion-name">
                {s.champion.driver}
              </h1>
              <div className="mt-4 text-xl text-neutral-300">
                campeão de <span className="text-[#E4FF00]">{data.year}</span> pela <span className="font-bold">{s.champion.team}</span>
              </div>
              {s.upset ? (
                <div className="mt-6 inline-block border border-[#FF3B30] text-[#FF3B30] px-3 py-1 label" data-testid="upset-badge">
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

      {/* News */}
      {news.length > 0 && (
        <section className="max-w-[1400px] mx-auto px-6 py-16 border-b border-[#262626]" data-testid="news-section">
          <div className="label text-[#E4FF00] mb-3">// COBERTURA IA</div>
          <h2 className="font-head font-black uppercase text-3xl sm:text-4xl tracking-tighter mb-10">
            Manchetes da temporada
          </h2>
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
                  <div className="absolute inset-0 bg-cover bg-center opacity-30 group-hover:opacity-40 transition-opacity"
                    style={{ backgroundImage: `url(${NEWS_IMGS[i % NEWS_IMGS.length]})` }} />
                  <div className="absolute inset-0 bg-gradient-to-t from-black via-black/80 to-black/40" />
                  <div className="relative flex flex-col h-full justify-end">
                    <div className="label text-[#E4FF00] mb-3">{n.tag || "F1"}</div>
                    <h3 className={`font-head font-black uppercase tracking-tighter leading-[0.95] mb-3 ${isBig ? "text-3xl sm:text-4xl lg:text-5xl" : "text-xl sm:text-2xl"}`}>
                      {n.title}
                    </h3>
                    {n.subtitle && <div className="text-neutral-300 text-sm mb-3">{n.subtitle}</div>}
                    {isBig && n.body && (
                      <div className="text-neutral-400 text-sm leading-relaxed whitespace-pre-line max-w-2xl">{n.body}</div>
                    )}
                  </div>
                </article>
              );
            })}
          </div>
        </section>
      )}

      {/* Standings */}
      <section className="max-w-[1400px] mx-auto px-6 py-16 border-b border-[#262626]">
        <div className="label text-[#E4FF00] mb-3">// CLASSIFICAÇÃO AO VIVO</div>
        <h2 className="font-head font-black uppercase text-3xl sm:text-4xl tracking-tighter mb-8">
          Pilotos & Construtores
        </h2>
        <StandingsCompact drivers={data.driver_standings} constructors={data.constructor_standings} />
        <div className="mt-4 label text-neutral-500">
          Sistema de pontos: {data.points_scheme.join("-")} (pontos por posição · era {data.year})
        </div>
      </section>

      {/* Race history */}
      <section className="max-w-[1400px] mx-auto px-6 py-16">
        <div className="label text-[#E4FF00] mb-3">// HISTÓRICO DE ETAPAS</div>
        <h2 className="font-head font-black uppercase text-3xl sm:text-4xl tracking-tighter mb-8">
          Corrida a corrida
        </h2>
        {data.races.length === 0 ? (
          <div className="border border-dashed border-[#262626] p-10 text-center">
            <div className="label text-neutral-500 mb-3">// AGUARDANDO PRIMEIRA CORRIDA</div>
            <p className="text-neutral-400 text-sm">
              Clique em <span className="text-[#E4FF00] font-bold">&quot;Simular Próxima →&quot;</span> acima para rodar a etapa {nextRoundNum} em {nextCircuit}.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4" data-testid="races-grid">
            {[...data.races].reverse().map((r) => (
              <RaceCard key={r.round} race={r} isLatest={r.round === latestRound} />
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
