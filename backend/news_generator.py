"""Template-based race news generator (no AI). Many variants per event type."""
import random

TAGS = ["CORRIDA", "GP", "DRAMA", "PISTA", "PÓDIO"]

TITLES_WIN = [
    "{d} DOMINA EM {c}",
    "VITÓRIA DE {d} EM {c}",
    "{d} VOA E VENCE EM {c}",
    "{c}: {d} NÃO DEIXA DÚVIDAS",
    "{d} CRAVA POLE-À-BANDEIRA EM {c}",
    "SHOW DE {d}: TRIUNFO EM {c}",
    "{d} SUPERA TUDO E VENCE EM {c}",
    "TRIUNFO DE {t} EM {c} COM {d}",
]
TITLES_LEADER_CHANGE = [
    "{d} ASSUME A LIDERANÇA DO MUNDIAL",
    "REVIRAVOLTA NO CAMPEONATO: {d} É O NOVO LÍDER",
    "{d} DESBANCA E LIDERA O MUNDIAL",
    "PONTA MUDA DE MÃOS: {d} É O NOVO LÍDER",
]
TITLES_DNF_HERO = [
    "DRAMA EM {c}: {dnf} ABANDONA",
    "{dnf} FICA PELO CAMINHO EM {c}",
    "ADEUS AO SONHO? {dnf} ABANDONA EM {c}",
    "PANE OU ACIDENTE: {dnf} SAI EM {c}",
]
TITLES_UPSET = [
    "SURPRESA EM {c}: {d} VENCE PELA {t}",
    "ZEBRA! {d} DA {t} VENCE EM {c}",
    "AZARÃO NO TOPO: {d} PELA {t} EM {c}",
]

BODY_WIN = [
    "{d} conduziu de forma impecável em {c} e cruzou a linha em primeiro pela {t}.\n\nCompletaram o pódio {p2} e {p3}. O resultado consolida a temporada da equipe e aumenta a expectativa para a próxima etapa.",
    "Domínio absoluto de {d} em {c}. O piloto da {t} venceu com folga em uma corrida sem grandes sustos.\n\nAtrás dele, {p2} e {p3} garantiram o pódio. A briga pelo campeonato ganha mais um capítulo.",
    "{d} venceu o GP de {c} pela {t} após uma prova estratégica. Segurou a pressão do início ao fim.\n\n{p2} completou em segundo, com {p3} em terceiro. A classificação geral segue apertada.",
    "Mais uma vitória para {d} em {c}. A {t} vive momento de graça na temporada.\n\n{p2} e {p3} completaram o pódio. O mundial pega fogo.",
]
BODY_LEADER = [
    "Com a vitória em {c}, {d} assume a liderança do campeonato mundial de pilotos.\n\nA {t} celebra o resultado e vislumbra uma temporada histórica. A próxima corrida promete.",
    "{d} chega à ponta do mundial após o triunfo em {c}. É o primeiro grande momento da campanha da {t}.\n\nOs adversários prometem reagir.",
]
BODY_UPSET = [
    "Uma vitória inesperada em {c}: {d}, correndo pela {t}, deixou os favoritos para trás.\n\nO resultado embaralha o campeonato e coloca a {t} no radar da temporada.",
    "Ninguém esperava, mas {d} venceu em {c} pela {t}. A corrida teve reviravoltas do começo ao fim.\n\nOs favoritos ficaram pra trás em uma tarde histórica.",
]
BODY_DNF = [
    "{dnf} teve que abandonar em {c} — mais um capítulo difícil na temporada. Enquanto isso, {d} aproveitou e venceu pela {t}.\n\nO pódio ficou com {p2} e {p3}. O mundial mudou de tom.",
    "Prejuízo enorme para {dnf} em {c}: DNF em corrida que poderia ter definido rumos. {d} lucrou e venceu.\n\nA {t} sai forte da etapa. Adversários que dormirem, perdem terreno.",
]


def _pick(seq):
    return random.choice(seq)


def generate_race_news_template(state: dict, race: dict) -> dict:
    """Deterministic-ish news based on race data using multiple templates."""
    rng = random.Random(
        (state.get("seed") or 0) * 31 + race.get("round", 0)
    )
    podium = race.get("podium") or []
    if not podium:
        return {"title": f"CAOS EM {race['circuit'].upper()}", "subtitle": f"Etapa {race['round']}",
                "body": "Corrida marcada por muitos abandonos, sem pódio registrado.", "tag": "DRAMA"}
    p1 = podium[0]
    p2 = podium[1]["driver"] if len(podium) > 1 else "—"
    p3 = podium[2]["driver"] if len(podium) > 2 else "—"
    dnfs = [r["driver"] for r in race.get("results", []) if r.get("dnf")]

    snap = race.get("standings_snapshot") or {}
    top = (snap.get("drivers") or [])[:2]
    leader_change = False
    if top and race.get("round", 0) > 1:
        # We don't have prev snapshot; approximate: if leader == winner and gap is small, mark change
        leader_change = top[0]["driver"] == p1["driver"] and race.get("round", 0) >= 2

    # Detect upset: winner rating below 90 or from a smaller team
    winner_data = next((d for d in state["drivers"] if d["name"] == p1["driver"]), None)
    is_upset = winner_data and winner_data.get("rating", 90) < 88

    # Choose template family
    r = rng.random()
    ctx = {"d": p1["driver"], "c": race["circuit"], "t": p1["team"], "p2": p2, "p3": p3,
           "dnf": dnfs[0] if dnfs else p1["driver"]}

    if is_upset and r < 0.7:
        title = rng.choice(TITLES_UPSET).format(**ctx)
        body = rng.choice(BODY_UPSET).format(**ctx)
        tag = "SURPRESA"
    elif dnfs and r < 0.35:
        title = rng.choice(TITLES_DNF_HERO).format(**ctx)
        body = rng.choice(BODY_DNF).format(**ctx)
        tag = "DRAMA"
    elif leader_change and r < 0.5:
        title = rng.choice(TITLES_LEADER_CHANGE).format(**ctx)
        body = rng.choice(BODY_LEADER).format(**ctx)
        tag = "CAMPEONATO"
    else:
        title = rng.choice(TITLES_WIN).format(**ctx)
        body = rng.choice(BODY_WIN).format(**ctx)
        tag = rng.choice(["CORRIDA", "GP", "PÓDIO"])

    subtitle = f"Etapa {race['round']} · {race['circuit']} · Pódio: {p1['driver']}, {p2}, {p3}"
    return {"title": title, "subtitle": subtitle, "body": body, "tag": tag}


# Replace AI functions with template variants
async def generate_race_news(state, race):
    return generate_race_news_template(state, race)


async def generate_news(simulation):
    """End-of-season wrap-up with a few templates."""
    s = simulation["summary"]
    champ = s["champion"]
    real = s["real_champion"]
    ctor = s["constructor_champion"]
    templates = [
        {"title": f"{champ['driver'].upper()} É CAMPEÃO DE {s['year']}",
         "subtitle": f"{champ['team']} celebra título mundial de pilotos",
         "body": f"{champ['driver']} conquistou o mundial de {s['year']} pela {champ['team']} somando {champ['points']} pontos. Na realidade histórica, o título ficou com {real['driver']}.",
         "tag": "CAMPEONATO"},
        {"title": f"{ctor['team'].upper()} DOMINA A TEMPORADA {s['year']}",
         "subtitle": f"Título de construtores com {ctor['points']} pts",
         "body": f"A {ctor['team']} conquistou o mundial de construtores em {s['year']}. Na história oficial, o título foi da {s['real_constructor_champion']}.",
         "tag": "EQUIPES"},
    ]
    return templates
