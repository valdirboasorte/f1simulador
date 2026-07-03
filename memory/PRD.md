# GRID/ALT · Simulador de Temporadas de F1 (Realidades Alternativas)

## Problem statement
"faz um simulador de temporadas de formula 1 que tenha todas as temporadas da historia da formula 1, simule resultados crie noticias dessas realidades alternativas que o usuario pode vê"

User choices:
- IA: Gemini 3 Flash (usando `gemini-3.5-flash` via Emergent LLM Key — `gemini-3-flash-preview` retornou erro de budget)
- Dataset: histórico completo 1950-2025 (76 temporadas)
- Motor: ratings dos pilotos + ruído gaussiano + chance de DNF (5%)
- Auth: sem login
- Idioma: português (Brasil)

## Architecture
- **Backend** (FastAPI + MongoDB + emergentintegrations)
  - `f1_data.py`: dicionário `SEASONS` com 76 temporadas (campeões reais, top ~10 pilotos por temporada com rating). `CIRCUITS_BY_ERA` para calendário.
  - `simulator.py`: motor stateful corrida-a-corrida. `points_scheme(year)` retorna sistema de pontos histórico.
  - `news_generator.py`: gera 4 notícias em pt-BR via `LlmChat` Gemini 3.5 Flash.
  - `server.py` endpoints (todos com prefixo `/api`):
    - `GET /seasons`, `GET /seasons/{year}`
    - `POST /simulate` (cria simulação vazia)
    - `POST /simulations/{id}/next` (roda próxima corrida)
    - `POST /simulations/{id}/finish` (roda todas as etapas restantes)
    - `POST /simulations/{id}/news` (gera manchetes IA — só após finished)
    - `GET /simulations/{id}`, `GET /simulations`
- **Frontend** (React + React Router + Tailwind)
  - `/` HomePage: hero + seletor por década + grid de temporadas
  - `/temporadas/:year` SeasonPage: informações da temporada + roster com ratings + botão "Iniciar Temporada"
  - `/simulacao/:id` SimulationPage: painel de comando fixo, standings ao vivo, histórico de etapas, seção de manchetes

## Pontuação histórica implementada
- 1950-1959: 8-6-4-3-2
- 1960: 8-6-4-3-2-1
- 1961-1990: 9-6-4-3-2-1
- 1991-2002: 10-6-4-3-2-1
- 2003-2009: 10-8-6-5-4-3-2-1
- 2010+: 25-18-15-12-10-8-6-4-2-1

## Implementado (2026-02)
- [x] Dataset 1950-2025 com todos os campeões reais
- [x] Motor de simulação race-by-race com seed
- [x] Pontuação por era histórica
- [x] Notícias IA em português
- [x] UI dark motorsport-editorial (Cabinet Grotesk + JetBrains Mono + Volt Yellow)
- [x] Progresso salvo no Mongo — usuário pode retomar
- [x] Botões "Simular Próxima" + "Rodar Tudo" + "Gerar Manchetes"

## Backlog / Próximos passos
- P1: Página `/historico` listando todas as simulações salvas
- P1: Comparativo lado-a-lado com campeonato real (posições reais vs simuladas)
- P1: Aumentar profundidade do dataset (mais pilotos por temporada, incluir voltas mais rápidas)
- P2: Compartilhamento (link público + card OG dinâmico com o veredito)
- P2: Personalizar rating de piloto antes de simular (modo "e se Senna estivesse na Williams em 1992?")
- P2: Sistema de conquistas / rankings entre simulações do mesmo usuário
- P2: Áudio de tema no hero + easter eggs por era
