import { Link, useLocation } from "react-router-dom";

const HERO_IMG =
  "https://images.unsplash.com/photo-1632726144626-6f6a8876e35d?crop=entropy&cs=srgb&fm=jpg&ixid=M3w4NjAzNDR8MHwxfHNlYXJjaHw0fHxmMSUyMHJhY2UlMjBjYXIlMjB0cmFjayUyMGRhcmt8ZW58MHx8fHwxNzgzMDQ5ODI3fDA&ixlib=rb-4.1.0&q=85";

export const Header = () => {
  const loc = useLocation();
  return (
    <header
      className="sticky top-0 z-30 border-b border-[#262626] backdrop-blur-xl bg-black/70"
      data-testid="app-header"
    >
      <div className="max-w-[1400px] mx-auto px-6 h-16 flex items-center justify-between">
        <Link to="/" className="flex items-center gap-3" data-testid="logo-link">
          <div className="w-2 h-8 bg-[#E4FF00]" />
          <div>
            <div className="font-head font-black text-lg leading-none tracking-tight">
              GRID/ALT
            </div>
            <div className="text-[10px] tracking-[0.22em] text-neutral-500 uppercase">
              F1 Alternate Reality
            </div>
          </div>
        </Link>
        <nav className="hidden sm:flex items-center gap-8 text-xs tracking-[0.22em] uppercase font-bold">
          <Link
            to="/"
            className={`hover:text-[#E4FF00] transition-colors ${loc.pathname === "/" ? "text-[#E4FF00]" : "text-neutral-300"}`}
            data-testid="nav-home"
          >
            Home
          </Link>
          <Link
            to="/temporadas"
            className={`hover:text-[#E4FF00] transition-colors ${loc.pathname.startsWith("/temporadas") ? "text-[#E4FF00]" : "text-neutral-300"}`}
            data-testid="nav-seasons"
          >
            Temporadas
          </Link>
        </nav>
      </div>
    </header>
  );
};

export const Hero = ({ onCta }) => (
  <section className="relative overflow-hidden border-b border-[#262626]">
    <div
      className="absolute inset-0 bg-cover bg-center"
      style={{ backgroundImage: `url(${HERO_IMG})` }}
    />
    <div className="absolute inset-0 bg-black/70" />
    <div className="relative max-w-[1400px] mx-auto px-6 py-24 sm:py-32 grid grid-cols-1 md:grid-cols-12 gap-8">
      <div className="md:col-span-8">
        <div className="label text-[#E4FF00] mb-6" data-testid="hero-label">
          // 1950 — 2025 · 76 TEMPORADAS
        </div>
        <h1 className="font-head font-black uppercase text-4xl sm:text-5xl lg:text-7xl leading-[0.9] tracking-tighter mb-6">
          E se a história<br />
          da <span className="text-[#E4FF00]">Fórmula 1</span><br />
          tivesse sido<br />
          <span className="line-through decoration-[#FF3B30] decoration-4">outra</span>?
        </h1>
        <p className="text-neutral-300 text-base sm:text-lg max-w-xl mb-10 leading-relaxed">
          Escolha qualquer temporada da história da F1, rode a simulação com
          ratings reais dos pilotos daquela era e leia as manchetes de uma
          realidade paralela — geradas por IA, em português.
        </p>
        <button
          onClick={onCta}
          data-testid="hero-cta-button"
          className="bg-[#E4FF00] text-black font-black uppercase tracking-[0.22em] text-sm px-8 py-5 hover:bg-[#C6DB00] transition-colors border-2 border-transparent focus:border-white outline-none"
        >
          Escolher Temporada →
        </button>
      </div>
      <div className="md:col-span-4 border-l border-[#262626] pl-8 hidden md:flex flex-col justify-between">
        <div>
          <div className="label mb-3">Modo</div>
          <div className="font-mono-num text-2xl leading-tight">
            ALT<br />REALITY<br />ENGINE
          </div>
        </div>
        <div>
          <div className="label mb-3">Fonte</div>
          <div className="text-neutral-400 text-sm">
            Ratings históricos +<br />ruído estocástico<br />
            <span className="text-[#E4FF00]">Gemini 3 Flash</span> p/ notícias
          </div>
        </div>
      </div>
    </div>
    {/* ticker */}
    <div className="relative border-t border-[#262626] bg-black overflow-hidden">
      <div className="ticker-track whitespace-nowrap py-3 text-xs tracking-[0.22em] uppercase text-neutral-500 font-bold">
        {Array.from({ length: 4 }).map((_, i) => (
          <span key={i} className="inline-block px-6">
            SENNA × PROST · SCHUMACHER × HAKKINEN · HAMILTON × VERSTAPPEN · FANGIO · CLARK · LAUDA · NORRIS × PIASTRI · BRABHAM · STEWART · VETTEL · ALONSO · ROSBERG × HAMILTON ·
          </span>
        ))}
      </div>
    </div>
  </section>
);
