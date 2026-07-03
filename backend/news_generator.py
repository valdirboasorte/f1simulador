"""News article generation via Gemini 3.5 Flash (Portuguese).

Two entry points:
- generate_race_news(state, race): one short article about a single race event
- generate_news(simulation): 4 wrap-up articles at end of season (legacy)
"""
import os
import json
import re
from emergentintegrations.llm.chat import LlmChat, UserMessage

_KEY = os.environ.get("EMERGENT_LLM_KEY")
_MODEL = ("gemini", "gemini-3.5-flash")


def _extract_json(text: str):
    text = text.strip()
    # try object first
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if m:
        try:
            return json.loads(m.group(0))
        except Exception:
            pass
    return None


def _race_prompt(state: dict, race: dict) -> str:
    year = state["year"]
    round_n = race["round"]
    total = state["total_races"]
    circuit = race["circuit"]
    podium = race["podium"]
    dnfs = [r for r in race["results"] if r.get("dnf")]
    snap = race.get("standings_snapshot") or {}
    top_drivers = (snap.get("drivers") or [])[:5]
    leader = top_drivers[0] if top_drivers else None
    second = top_drivers[1] if len(top_drivers) > 1 else None
    gap = (leader["points"] - second["points"]) if leader and second else 0

    podium_txt = ", ".join(
        f"{p['position']}º {p['driver']} ({p['team']})" for p in podium
    ) or "sem pódio"
    dnf_txt = ", ".join(d["driver"] for d in dnfs[:4]) or "nenhum abandono relevante"
    top_txt = " | ".join(
        f"{i+1}º {d['driver']} {d['points']}pt" for i, d in enumerate(top_drivers)
    )

    return f"""Você é jornalista esportivo brasileiro cobrindo AO VIVO a temporada {year} de F1 em uma REALIDADE ALTERNATIVA.

CORRIDA ATUAL: Etapa {round_n}/{total} · {circuit}
Pódio: {podium_txt}
Abandonos: {dnf_txt}
Classificação após esta corrida: {top_txt}
Vantagem do líder: {gap} pts

TAREFA: Escreva UMA notícia curta em PORTUGUÊS DO BRASIL sobre ESTA corrida específica. Tom de jornal esportivo, dramático mas factual. Retorne APENAS um JSON (sem markdown, sem ```), nesta estrutura:
{{"title": "manchete de até 90 chars", "subtitle": "linha fina", "body": "2 parágrafos curtos separados por \\n\\n", "tag": "CORRIDA"}}

Regras:
- Cite APENAS pilotos e equipes que aparecem acima.
- A notícia deve refletir o evento REAL desta corrida (vencedor, disputa, DNF marcante ou mudança na liderança).
- NÃO inventar.
- Retorne SÓ o JSON."""


async def generate_race_news(state: dict, race: dict) -> dict:
    """Return a single news dict {title, subtitle, body, tag}."""
    if not _KEY:
        return _fallback_race_news(race)
    try:
        chat = LlmChat(
            api_key=_KEY,
            session_id=f"f1-race-{state['year']}-{race['round']}-{state.get('seed', 0)}",
            system_message="Você é redator do jornal esportivo GRID no Brasil, especialista em F1.",
        ).with_model(*_MODEL)
        response = await chat.send_message(UserMessage(text=_race_prompt(state, race)))
        text = response if isinstance(response, str) else str(response)
        data = _extract_json(text)
        if isinstance(data, dict) and data.get("title"):
            data.setdefault("tag", "CORRIDA")
            data.setdefault("subtitle", "")
            data.setdefault("body", "")
            return data
    except Exception as e:
        print(f"[race-news] error: {e}")
    return _fallback_race_news(race)


def _fallback_race_news(race: dict) -> dict:
    if race["podium"]:
        w = race["podium"][0]
        title = f"{w['driver'].upper()} VENCE EM {race['circuit'].upper()}"
        body = f"{w['driver']} cruzou a linha de chegada em primeiro no GP disputado em {race['circuit']}, marcando mais uma vitória para a {w['team']}.\n\nA corrida teve pódio completado por " + \
               ", ".join(f"{p['driver']}" for p in race["podium"][1:]) + "."
    else:
        title = f"CAOS EM {race['circuit'].upper()}"
        body = f"A etapa {race['round']} em {race['circuit']} terminou sem pódio registrado."
    return {"title": title, "subtitle": f"Etapa {race['round']}", "body": body, "tag": "CORRIDA"}


# ---- Legacy season wrap-up (kept for optional call) ----

def _wrap_prompt(simulation: dict) -> str:
    s = simulation["summary"]
    year = s["year"]
    champion = s["champion"]
    real = s["real_champion"]
    runner = s["runner_up"]
    ctor = s["constructor_champion"]
    top5 = simulation["driver_standings"][:5]
    top5_lines = [
        f"{i+1}º {d['driver']} ({d['team']}) — {d['points']} pts, {d['wins']} vit."
        for i, d in enumerate(top5)
    ]
    upset = "SIM" if s["upset"] else "NÃO"
    return f"""Cobertura pós-temporada F1 {year} em realidade alternativa.
- Campeão: {champion['driver']} ({champion['team']}) {champion['points']} pts
- Vice: {runner['driver']} ({runner['team']}) {runner['points']} pts
- Real: {real['driver']}
- Reviravolta? {upset}
- Construtores: {ctor['team']} — {ctor['points']} pts

TOP 5:
{chr(10).join(top5_lines)}

Retorne APENAS um JSON array com 3 notícias em pt-BR:
[{{"title":"...","subtitle":"...","body":"2-3 parágrafos","tag":"CAMPEONATO|EQUIPES|ANÁLISE"}}]"""


async def generate_news(simulation: dict) -> list[dict]:
    if not _KEY:
        return []
    try:
        chat = LlmChat(
            api_key=_KEY,
            session_id=f"f1-wrap-{simulation['year']}-{simulation.get('seed', 0)}",
            system_message="Você é redator sênior do GRID cobrindo F1.",
        ).with_model(*_MODEL)
        response = await chat.send_message(UserMessage(text=_wrap_prompt(simulation)))
        text = response if isinstance(response, str) else str(response)
        data = _extract_json(text)
        if isinstance(data, list) and data:
            return data
    except Exception as e:
        print(f"[wrap-news] error: {e}")
    return []
