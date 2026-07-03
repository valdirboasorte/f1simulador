"""News article generation via Gemini 3 Flash (in Portuguese)."""
import os
import json
import re
from emergentintegrations.llm.chat import LlmChat, UserMessage

_KEY = os.environ.get("EMERGENT_LLM_KEY")


def _build_prompt(simulation: dict) -> str:
    s = simulation["summary"]
    year = s["year"]
    champion = s["champion"]
    real = s["real_champion"]
    runner = s["runner_up"]
    ctor = s["constructor_champion"]
    real_ctor = s["real_constructor_champion"]

    # Sample a few races (first, mid, last, and any surprise winner)
    races = simulation["races"]
    sample = []
    if races:
        sample.append(races[0])
        sample.append(races[len(races) // 2])
        sample.append(races[-1])
    race_lines = []
    for r in sample:
        if r["podium"]:
            p = r["podium"]
            race_lines.append(
                f"- Etapa {r['round']} ({r['circuit']}): 1º {p[0]['driver']} ({p[0]['team']})"
                + (f", 2º {p[1]['driver']}" if len(p) > 1 else "")
                + (f", 3º {p[2]['driver']}" if len(p) > 2 else "")
            )
    top5 = simulation["driver_standings"][:5]
    top5_lines = [
        f"{i+1}º {d['driver']} ({d['team']}) — {d['points']} pts, {d['wins']} vitórias"
        for i, d in enumerate(top5)
    ]

    upset = "SIM" if s["upset"] else "NÃO"

    return f"""Você é um jornalista esportivo brasileiro cobrindo a temporada {year} de Fórmula 1 em uma realidade alternativa.

DADOS DA TEMPORADA SIMULADA {year}:
- Campeão simulado: {champion['driver']} ({champion['team']}) — {champion['points']} pontos, {champion['wins']} vitórias
- Vice: {runner['driver']} ({runner['team']}) — {runner['points']} pts
- Campeão real histórico: {real['driver']} ({real['team']})
- É uma REVIRAVOLTA vs realidade? {upset}
- Construtores simulado: {ctor['team']} — {ctor['points']} pts
- Construtores real: {real_ctor}

TOP 5 SIMULADO:
{chr(10).join(top5_lines)}

CORRIDAS DE DESTAQUE:
{chr(10).join(race_lines)}

TAREFA: Escreva 4 notícias curtas em PORTUGUÊS DO BRASIL, com tom de jornal esportivo, dramático mas realista. Retorne APENAS um JSON válido (sem markdown, sem ```), no formato:
[
  {{"title": "manchete impactante", "subtitle": "linha fina descritiva", "body": "3-4 parágrafos separados por \\n\\n", "tag": "CAMPEONATO|CORRIDA|EQUIPES|ANÁLISE"}},
  ...
]

Regras:
- Manchetes em CAIXA ALTA parcial permitido, curtas (max 90 caracteres).
- Corpo: 3-4 parágrafos, factual mas com narrativa. Cite pilotos, equipes, circuitos.
- Uma notícia deve ser sobre o campeão, uma sobre a disputa de construtores, uma sobre uma corrida marcante, e uma análise geral da temporada.
- NÃO invente pilotos que não estejam na lista. Use apenas os nomes fornecidos.
- Retorne APENAS o JSON, sem texto adicional."""


async def generate_news(simulation: dict) -> list[dict]:
    if not _KEY:
        return _fallback_news(simulation)

    prompt = _build_prompt(simulation)
    try:
        chat = LlmChat(
            api_key=_KEY,
            session_id=f"f1-news-{simulation['year']}-{simulation.get('seed', 0)}",
            system_message="Você é um jornalista esportivo especializado em Fórmula 1, redator do jornal 'GRID' no Brasil.",
        ).with_model("gemini", "gemini-3.5-flash")
        response = await chat.send_message(UserMessage(text=prompt))
        text = response if isinstance(response, str) else str(response)
        # extract JSON
        match = re.search(r"\[.*\]", text, re.DOTALL)
        if match:
            data = json.loads(match.group(0))
            if isinstance(data, list) and data:
                return data
    except Exception as e:
        print(f"[news] error: {e}")

    return _fallback_news(simulation)


def _fallback_news(simulation: dict) -> list[dict]:
    s = simulation["summary"]
    champ = s["champion"]
    real = s["real_champion"]
    ctor = s["constructor_champion"]
    return [
        {
            "title": f"{champ['driver'].upper()} É CAMPEÃO EM {s['year']}",
            "subtitle": f"Em realidade alternativa, {champ['team']} domina o mundial",
            "body": f"{champ['driver']} conquistou o título mundial de {s['year']} pela equipe {champ['team']}, somando {champ['points']} pontos ao longo da temporada.\n\nNa história oficial, o troféu foi para {real['driver']} ({real['team']}). Nesta simulação, o resultado foi outro.\n\nA temporada teve {s['num_races']} etapas e uma disputa que só se definiu nas últimas corridas.",
            "tag": "CAMPEONATO",
        },
        {
            "title": f"{ctor['team'].upper()} LEVA O MUNDIAL DE CONSTRUTORES",
            "subtitle": f"Equipe soma {ctor['points']} pontos na temporada simulada",
            "body": f"A {ctor['team']} garantiu o título de construtores de {s['year']} nesta realidade alternativa.\n\nHistoricamente, o título ficou com {s['real_constructor_champion']}.\n\nA campanha da equipe foi consistente do primeiro ao último GP.",
            "tag": "EQUIPES",
        },
    ]
