import { useEffect, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import {
  createReality,
  listRealities,
  fetchReality,
  createSimulation,
} from "../lib/api";
import { Header } from "../components/Layout";

const rankBy = (obj, field) =>
  Object.entries(obj)
    .map(([k, v]) => ({ name: k, ...v }))
    .sort((a, b) => (b[field] || 0) - (a[field] || 0))
    .slice(0, 12);

export const RealityListPage = () => {
  const [items, setItems] = useState([]);
  const [name, setName] = useState("");
  const [creating, setCreating] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    listRealities().then(setItems).catch(() => {});
  }, []);

  const onCreate = async () => {
    setCreating(true);
    try {
      const r = await createReality(name || "Minha Realidade");
      navigate(`/realidade/${r.id}`);
    } finally {
      setCreating(false);
    }
  };

  return (
    <div>
      <Header />
      <section className="max-w-[1000px] mx-auto px-6 py-20">
        <div className="label text-[#E4FF00] mb-3">// MODO CAMPANHA</div>
        <h1 className="font-head font-black uppercase text-4xl sm:text-6xl tracking-tighter leading-[0.9] mb-6">
          Minha Realidade
        </h1>
        <p className="text-neutral-400 text-sm max-w-xl mb-10 leading-relaxed">
          Comece em 1950 e simule cada temporada em ordem cronológica até 2025.
          Vitórias, pódios e títulos vão sendo acumulados por piloto e equipe,
          criando uma linha do tempo alternativa exclusivamente sua.
        </p>

        <div className="border border-[#262626] p-6 mb-10">
          <div className="label mb-3">Criar nova realidade</div>
          <div className="flex flex-col sm:flex-row gap-3">
            <input
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Nome da sua realidade (ex: Timeline #01)"
              data-testid="reality-name-input"
              className="flex-1 bg-[#0A0A0A] border border-[#262626] px-4 py-3 text-sm text-white placeholder:text-neutral-600 focus:border-[#E4FF00] outline-none"
            />
            <button
              onClick={onCreate}
              disabled={creating}
              data-testid="create-reality-button"
              className="bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-xs px-8 py-3 hover:bg-[#C6DB00] disabled:opacity-50"
            >
              {creating ? "Criando..." : "Começar em 1950 →"}
            </button>
          </div>
        </div>

        <div className="label mb-3">Realidades salvas</div>
        {items.length === 0 ? (
          <div className="text-neutral-500 text-sm">Nenhuma ainda.</div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-px bg-[#262626] border border-[#262626]">
            {items.map((r) => (
              <Link
                key={r.id}
                to={`/realidade/${r.id}`}
                data-testid={`reality-item-${r.id}`}
                className="bg-[#0A0A0A] p-5 hover:bg-[#141414] group"
              >
                <div className="flex justify-between items-baseline mb-2">
                  <div className="font-head font-black uppercase text-lg tracking-tight">
                    {r.name}
                  </div>
                  <div className="font-mono-num text-xs text-[#E4FF00]">
                    {r.finished ? "COMPLETA" : `${r.current_year}`}
                  </div>
                </div>
                <div className="text-neutral-500 text-xs">
                  {r.seasons?.length || 0} temporadas registradas
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

export const RealityDetailPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [reality, setReality] = useState(null);
  const [starting, setStarting] = useState(false);

  useEffect(() => {
    fetchReality(id).then(setReality).catch(() => setReality(false));
  }, [id]);

  const startYear = async () => {
    setStarting(true);
    try {
      const sim = await createSimulation(reality.current_year, undefined, reality.id);
      navigate(`/simulacao/${sim.id}`);
    } finally {
      setStarting(false);
    }
  };

  if (reality === false) {
    return (
      <div>
        <Header />
        <div className="p-10 text-center text-[#FF3B30]">Realidade não encontrada</div>
      </div>
    );
  }
  if (!reality) {
    return (
      <div>
        <Header />
        <div className="p-10 text-neutral-500 font-mono-num">Carregando...</div>
      </div>
    );
  }

  const driversByChampionships = rankBy(reality.driver_stats, "championships");
  const driversByWins = rankBy(reality.driver_stats, "wins");
  const constructorsByTitles = rankBy(reality.constructor_stats, "championships");
  const progress = ((reality.seasons.length) / (2025 - 1950 + 1)) * 100;

  return (
    <div>
      <Header />
      <section className="border-b border-[#262626]">
        <div className="max-w-[1400px] mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-12 gap-8 items-end">
          <div className="md:col-span-8">
            <Link to="/realidade" className="label text-neutral-500 hover:text-[#E4FF00]">← Realidades</Link>
            <div className="label text-[#E4FF00] mt-4 mb-2">// MINHA REALIDADE</div>
            <h1 className="font-head font-black uppercase text-4xl sm:text-6xl tracking-tighter leading-[0.9]" data-testid="reality-name">
              {reality.name}
            </h1>
            <div className="mt-6 flex flex-wrap gap-8 text-sm">
              <div>
                <div className="label mb-1">Ano atual</div>
                <div className="font-mono-num text-3xl font-bold text-[#E4FF00]" data-testid="reality-current-year">
                  {reality.finished ? "2025 ✓" : reality.current_year}
                </div>
              </div>
              <div>
                <div className="label mb-1">Temporadas</div>
                <div className="font-mono-num text-3xl font-bold">
                  {reality.seasons.length}<span className="text-neutral-600 text-lg">/76</span>
                </div>
              </div>
            </div>
            <div className="mt-4 h-2 bg-[#1F1F1F] max-w-md">
              <div className="h-full bg-[#E4FF00]" style={{ width: `${progress}%` }} />
            </div>
          </div>
          <div className="md:col-span-4">
            {!reality.finished ? (
              <button
                onClick={startYear}
                disabled={starting}
                data-testid="start-year-button"
                className="w-full bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-sm py-6 hover:bg-[#C6DB00] disabled:opacity-50"
              >
                {starting ? "Preparando..." : `▶ Rodar ${reality.current_year}`}
              </button>
            ) : (
              <div className="text-center label text-[#00FF66] py-6 border border-[#00FF66]">
                ✓ TIMELINE COMPLETA (1950—2025)
              </div>
            )}
          </div>
        </div>
      </section>

      {/* Records */}
      {reality.seasons.length > 0 ? (
        <section className="max-w-[1400px] mx-auto px-6 py-12 grid grid-cols-1 md:grid-cols-3 gap-6">
          <RankCard title="Mais Títulos (Pilotos)" items={driversByChampionships} field="championships" testid="rank-champions" />
          <RankCard title="Mais Vitórias (Pilotos)" items={driversByWins} field="wins" testid="rank-wins" />
          <RankCard title="Títulos de Construtores" items={constructorsByTitles} field="championships" testid="rank-constructors" />
        </section>
      ) : (
        <section className="max-w-[1400px] mx-auto px-6 py-16 text-neutral-500 text-sm text-center border border-dashed border-[#262626] mx-6 my-10">
          Nenhuma temporada registrada ainda. Rode {reality.current_year} para começar sua timeline.
        </section>
      )}

      {/* Season log */}
      <section className="max-w-[1400px] mx-auto px-6 py-12 border-t border-[#262626]">
        <div className="label text-[#E4FF00] mb-3">// LINHA DO TEMPO</div>
        <h2 className="font-head font-black uppercase text-3xl tracking-tighter mb-8">
          Temporadas registradas
        </h2>
        {reality.seasons.length === 0 ? (
          <div className="text-neutral-500 text-sm">—</div>
        ) : (
          <div className="border border-[#262626]" data-testid="seasons-log">
            <div className="grid grid-cols-12 gap-4 px-4 py-2 border-b border-[#262626] label bg-[#141414]">
              <div className="col-span-1">Ano</div>
              <div className="col-span-4">Campeão simulado</div>
              <div className="col-span-3">Construtores</div>
              <div className="col-span-3">Campeão real</div>
              <div className="col-span-1 text-right">Diff</div>
            </div>
            {[...reality.seasons].reverse().map((s) => (
              <Link
                key={s.year}
                to={`/simulacao/${s.sim_id}`}
                className="grid grid-cols-12 gap-4 px-4 py-2.5 border-b border-[#262626] items-center text-sm hover:bg-[#141414]"
                data-testid={`season-log-${s.year}`}
              >
                <div className="col-span-1 font-mono-num text-[#E4FF00]">{s.year}</div>
                <div className="col-span-4 font-head font-bold uppercase tracking-tight">
                  {s.champion?.driver} <span className="text-neutral-500 font-normal text-xs">({s.champion?.team})</span>
                </div>
                <div className="col-span-3 text-sm">{s.constructor_champion?.team}</div>
                <div className="col-span-3 text-neutral-500 text-xs">{s.real_champion}</div>
                <div className={`col-span-1 text-right text-xs ${s.upset ? "text-[#FF3B30]" : "text-[#00FF66]"}`}>
                  {s.upset ? "ALT" : "OK"}
                </div>
              </Link>
            ))}
          </div>
        )}
      </section>
    </div>
  );
};

const RankCard = ({ title, items, field, testid }) => (
  <div className="border border-[#262626]" data-testid={testid}>
    <div className="label bg-[#141414] px-4 py-3 border-b border-[#262626]">{title}</div>
    {items.length === 0 && <div className="p-4 text-neutral-500 text-xs">—</div>}
    {items.slice(0, 8).map((x, i) => (
      <div key={x.name} className={`flex justify-between px-4 py-2 border-b border-[#262626] text-sm ${i === 0 ? "text-[#E4FF00]" : ""}`}>
        <span className="font-head font-bold uppercase tracking-tight text-xs truncate">
          <span className="font-mono-num text-neutral-500 mr-2">{i + 1}.</span>
          {x.name}
        </span>
        <span className="font-mono-num font-bold text-xs">{x[field] || 0}</span>
      </div>
    ))}
  </div>
);

export default RealityListPage;
