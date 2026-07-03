"""Historical What-If events. Effects can span the entire timeline (until 9999)
and are enforced with a max of 2 drivers per team per season."""

EVENTS = {
    1955: {
        "id": "lemans_1955", "title": "Le Mans 1955 · Desastre e retirada da Mercedes",
        "description": "84 mortos em Le Mans. Mercedes se retira do automobilismo ao fim de 1955.",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Mercedes se retira ao fim de 1955.", "effects": []},
            {"id": "stay", "label": "Mercedes segue na F1", "detail": "Fangio permanece na Mercedes até se aposentar; Moss os acompanha.", "effects": [
                {"type": "team_override", "driver": "Juan Manuel Fangio", "team": "Mercedes", "from_year": 1956, "until_year": 1958, "rating": 96},
                {"type": "team_override", "driver": "Stirling Moss", "team": "Mercedes", "from_year": 1956, "until_year": 1961, "rating": 95},
                {"type": "rating_delta", "driver": "Juan Manuel Fangio", "delta": 2, "from_year": 1956, "until_year": 1958},
            ]},
        ],
    },
    1968: {
        "id": "clark_1968", "title": "Hockenheim 1968 · Jim Clark",
        "description": "Abril de 1968. Clark morre em corrida de F2 em Hockenheim. E se ele tivesse continuado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Clark morre; Graham Hill assume o mundial.", "effects": [{"type": "remove_driver_from", "driver": "Jim Clark", "from_year": 1968}]},
            {"id": "survives", "label": "Clark sobrevive", "detail": "Continua na Lotus até ~1975, disputando com Stewart.", "effects": [
                {"type": "team_override", "driver": "Jim Clark", "team": "Lotus", "from_year": 1968, "until_year": 1975, "rating": 97},
                {"type": "rating_delta", "driver": "Jim Clark", "delta": 3, "from_year": 1968, "until_year": 1975},
            ]},
        ],
    },
    1970: {
        "id": "rindt_1970", "title": "Monza 1970 · Jochen Rindt",
        "description": "Rindt morre em Monza — único campeão póstumo. E se sobrevivesse?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Único campeão póstumo.", "effects": [{"type": "remove_driver_from", "driver": "Jochen Rindt", "from_year": 1971}]},
            {"id": "survives", "label": "Rindt sobrevive", "detail": "Segue como piloto de elite até fim dos anos 70.", "effects": [
                {"type": "team_override", "driver": "Jochen Rindt", "team": "Lotus", "from_year": 1971, "until_year": 1978, "rating": 95},
                {"type": "rating_delta", "driver": "Jochen Rindt", "delta": 4, "from_year": 1971, "until_year": 1978},
            ]},
        ],
    },
    1976: {
        "id": "lauda_1976", "title": "Nürburgring 1976 · Niki Lauda",
        "description": "Lauda por pouco não morre em Nürburgring. Volta seis semanas depois.",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Perde o título por 1 pt.", "effects": []},
            {"id": "fatal", "label": "Lauda morre", "detail": "Hunt vence com folga. Ferrari perde seu piloto símbolo.", "effects": [{"type": "remove_driver_from", "driver": "Niki Lauda", "from_year": 1977}]},
            {"id": "avoids", "label": "Lauda evita o acidente", "detail": "Domina o fim dos 70 sem sequelas.", "effects": [
                {"type": "rating_delta", "driver": "Niki Lauda", "delta": 4, "from_year": 1976, "until_year": 1985},
            ]},
        ],
    },
    1978: {
        "id": "peterson_1978", "title": "Monza 1978 · Ronnie Peterson",
        "description": "Peterson morre após acidente na largada em Monza. E se sobrevivesse?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Peterson morre.", "effects": [{"type": "remove_driver_from", "driver": "Ronnie Peterson", "from_year": 1979}]},
            {"id": "survives", "label": "Peterson sobrevive", "detail": "Segue na Lotus/McLaren no início dos 80.", "effects": [
                {"type": "team_override", "driver": "Ronnie Peterson", "team": "McLaren", "from_year": 1979, "until_year": 1984, "rating": 92},
            ]},
        ],
    },
    1982: {
        "id": "villeneuve_1982", "title": "Zolder 1982 · Gilles Villeneuve",
        "description": "Villeneuve morre em Zolder. E se sobrevivesse?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Ferrari perde seu ídolo.", "effects": [{"type": "remove_driver_from", "driver": "Gilles Villeneuve", "from_year": 1982}]},
            {"id": "survives", "label": "Villeneuve sobrevive", "detail": "Fica na Ferrari até 1988, brigando por títulos.", "effects": [
                {"type": "team_override", "driver": "Gilles Villeneuve", "team": "Ferrari", "from_year": 1982, "until_year": 1988, "rating": 93},
                {"type": "rating_delta", "driver": "Gilles Villeneuve", "delta": 3, "from_year": 1982, "until_year": 1988},
            ]},
        ],
    },
    1993: {
        "id": "prost_1993", "title": "Fim de 1993 · Aposentadoria de Prost",
        "description": "Prost se aposenta após o tetra. E se tivesse ficado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Prost se aposenta.", "effects": [{"type": "remove_driver_from", "driver": "Alain Prost", "from_year": 1994}]},
            {"id": "stays", "label": "Prost continua na Williams", "detail": "Duelo Prost × Senna dentro da Williams em 1994.", "effects": [
                {"type": "team_override", "driver": "Alain Prost", "team": "Williams", "from_year": 1994, "until_year": 1996, "rating": 95},
            ]},
        ],
    },
    1994: {
        "id": "senna_1994", "title": "Imola 1994 · Ayrton Senna",
        "description": "Senna morre em Imola. E se sobrevivesse?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Senna morre.", "effects": [{"type": "remove_driver_from", "driver": "Ayrton Senna", "from_year": 1995}]},
            {"id": "survives_ferrari", "label": "Senna sobrevive → Ferrari em 96", "detail": "Vai para a Ferrari em 96 (Schumacher fica na Benetton até 2000).", "effects": [
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Williams", "from_year": 1994, "until_year": 1995, "rating": 97},
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Ferrari", "from_year": 1996, "until_year": 2004, "rating": 96},
                {"type": "team_override", "driver": "Michael Schumacher", "team": "Benetton", "from_year": 1996, "until_year": 2000, "rating": 96},
            ]},
            {"id": "survives_stays", "label": "Senna sobrevive → fica na Williams", "detail": "Domina os anos 90 pela Williams.", "effects": [
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Williams", "from_year": 1994, "until_year": 2003, "rating": 97},
            ]},
        ],
    },
    2006: {
        "id": "schumi_2006", "title": "Fim de 2006 · Aposentadoria de Schumacher",
        "description": "Schumacher se aposenta. E se tivesse ficado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Kimi assume a Ferrari em 2007.", "effects": [{"type": "remove_driver_from", "driver": "Michael Schumacher", "from_year": 2007}]},
            {"id": "stays", "label": "Schumi fica até 2012", "detail": "Ferrari mantém o alemão; Kimi vai para outra equipe.", "effects": [
                {"type": "team_override", "driver": "Michael Schumacher", "team": "Ferrari", "from_year": 2007, "until_year": 2012, "rating": 96},
            ]},
        ],
    },
    2008: {
        "id": "singapore_gate", "title": "Cingapura 2008 · Crashgate",
        "description": "Piquet Jr. bate propositalmente para Alonso vencer. E se não tivesse rolado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Alonso vence com auxílio.", "effects": []},
            {"id": "clean", "label": "Renault joga limpo", "detail": "Massa vence Cingapura e chega ao final com mais vantagem sobre Hamilton.", "effects": [
                {"type": "rating_delta", "driver": "Felipe Massa", "delta": 3, "from_year": 2008, "until_year": 2008},
                {"type": "rating_delta", "driver": "Fernando Alonso", "delta": -2, "from_year": 2008, "until_year": 2008},
            ]},
        ],
    },
    2013: {
        "id": "kimi_2013", "title": "Fim de 2013 · Retorno de Kimi",
        "description": "Kimi voltou à Ferrari em 2014 formando dupla com Alonso. E se ele tivesse ficado na Lotus?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Kimi na Ferrari 2014.", "effects": []},
            {"id": "stays_lotus", "label": "Kimi fica na Lotus", "detail": "Ferrari fica com outra dupla; Kimi extrai mais da Lotus.", "effects": [
                {"type": "team_override", "driver": "Kimi Raikkonen", "team": "Lotus", "from_year": 2014, "until_year": 2017, "rating": 90},
            ]},
        ],
    },
    2014: {
        "id": "alonso_ferrari_2014", "title": "Fim de 2014 · Alonso deixa a Ferrari?",
        "description": "Alonso trocou a Ferrari pela McLaren-Honda em 2015 — desastre. E se ele tivesse ficado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Alonso vai para McLaren-Honda; Vettel à Ferrari.", "effects": []},
            {"id": "stays", "label": "Alonso fica na Ferrari", "detail": "Vettel permanece na Red Bull; Alonso disputa com Hamilton.", "effects": [
                {"type": "team_override", "driver": "Fernando Alonso", "team": "Ferrari", "from_year": 2015, "until_year": 2020, "rating": 94},
                {"type": "team_override", "driver": "Sebastian Vettel", "team": "Red Bull", "from_year": 2015, "until_year": 2018, "rating": 93},
            ]},
        ],
    },
    2016: {
        "id": "rosberg_2016", "title": "Fim de 2016 · Rosberg se aposenta",
        "description": "Rosberg anuncia aposentadoria dias após o título. E se continuasse?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Bottas assume a Mercedes.", "effects": [{"type": "remove_driver_from", "driver": "Nico Rosberg", "from_year": 2017}]},
            {"id": "stays", "label": "Rosberg continua até 2022", "detail": "Duelo Hamilton × Rosberg segue por anos.", "effects": [
                {"type": "team_override", "driver": "Nico Rosberg", "team": "Mercedes", "from_year": 2017, "until_year": 2022, "rating": 92},
            ]},
        ],
    },
}


def event_for_year(year: int, resolved_ids: list[str]) -> dict | None:
    ev = EVENTS.get(year)
    if not ev or ev["id"] in resolved_ids:
        return None
    return ev


def apply_effects(drivers: list[dict], year: int, effects: list[dict]) -> list[dict]:
    """Apply cumulative effects + enforce realism (max 2 drivers per team)."""
    roster = {d["name"]: dict(d) for d in drivers}
    protected: set[str] = set()  # drivers placed by team_override (or added)

    for eff in effects:
        t = eff["type"]
        fy = eff.get("from_year", 0)
        uy = eff.get("until_year", 9999)
        if not (fy <= year <= uy):
            continue
        name = eff["driver"]
        if t == "remove_driver_from":
            roster.pop(name, None)
        elif t == "team_override":
            if name in roster:
                roster[name]["team"] = eff["team"]
            else:
                roster[name] = {"name": name, "team": eff["team"], "rating": eff.get("rating", 92)}
            protected.add(name)
        elif t == "rating_delta" and name in roster:
            roster[name]["rating"] = max(50, min(99, roster[name]["rating"] + eff["delta"]))

    # Realism: max 2 drivers per team. Displace the lowest-rated non-protected driver.
    from collections import defaultdict
    by_team = defaultdict(list)
    for d in roster.values():
        by_team[d["team"]].append(d)
    to_remove: list[str] = []
    for team, ds in by_team.items():
        if len(ds) <= 2:
            continue
        # Sort: protected first (keep), then by rating desc
        ds.sort(key=lambda d: (d["name"] in protected, d["rating"]), reverse=True)
        for d in ds[2:]:
            to_remove.append(d["name"])
    for n in to_remove:
        roster.pop(n, None)

    return list(roster.values())
