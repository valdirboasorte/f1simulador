"""Historical 'What If' events for MINHA REALIDADE mode.

Each event is triggered when the reality reaches the given year. The user picks
one choice, and its `effects` are stored on the reality and applied to the
roster of that year (and future years) when simulating.

Effect types:
  - remove_driver_from: driver disappears from `from_year` onwards
  - team_override: driver switches to `team` from `from_year` up to `until_year`
  - rating_delta: driver's rating adjusted by `delta` during range
"""

EVENTS = {
    1955: {
        "id": "lemans_1955",
        "title": "Le Mans 1955 · Desastre e retirada da Mercedes",
        "description": "O acidente de Le Mans matou 84 pessoas. Mercedes se retira do automobilismo no fim da temporada. E se a Mercedes tivesse continuado na F1?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Mercedes se retira ao fim de 1955.", "effects": []},
            {"id": "stay", "label": "Mercedes segue na F1", "detail": "Fangio segue na Mercedes até 1958.", "effects": [
                {"type": "team_override", "driver": "Juan Manuel Fangio", "team": "Mercedes", "from_year": 1956, "until_year": 1958},
                {"type": "rating_delta", "driver": "Juan Manuel Fangio", "delta": 2, "from_year": 1956, "until_year": 1958},
            ]},
        ],
    },
    1970: {
        "id": "rindt_1970",
        "title": "Monza 1970 · Jochen Rindt",
        "description": "5 de setembro. Rindt bate mortalmente durante os treinos em Monza — se torna campeão póstumo. E se ele tivesse sobrevivido?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Rindt morre em Monza. Único campeão póstumo.", "effects": [
                {"type": "remove_driver_from", "driver": "Jochen Rindt", "from_year": 1971}
            ]},
            {"id": "survives", "label": "Rindt sobrevive", "detail": "Continua na Lotus até 1974, disputa títulos com Stewart.", "effects": [
                {"type": "team_override", "driver": "Jochen Rindt", "team": "Lotus", "from_year": 1971, "until_year": 1974},
                {"type": "rating_delta", "driver": "Jochen Rindt", "delta": 4, "from_year": 1971, "until_year": 1974},
            ]},
        ],
    },
    1976: {
        "id": "lauda_1976",
        "title": "Nürburgring 1976 · Niki Lauda",
        "description": "1 de agosto. Lauda sofre queimaduras terríveis em Nürburgring e por pouco não morre. Volta a correr apenas 6 semanas depois.",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Lauda perde o título por 1 ponto para Hunt.", "effects": []},
            {"id": "fatal", "label": "Lauda morre no acidente", "detail": "James Hunt vence com folga; Ferrari perde seu piloto símbolo dos anos 70.", "effects": [
                {"type": "remove_driver_from", "driver": "Niki Lauda", "from_year": 1977}
            ]},
            {"id": "avoids", "label": "Lauda evita o acidente", "detail": "Termina 1976 forte e vira tricampeão nos anos seguintes.", "effects": [
                {"type": "rating_delta", "driver": "Niki Lauda", "delta": 4, "from_year": 1976, "until_year": 1979}
            ]},
        ],
    },
    1982: {
        "id": "villeneuve_1982",
        "title": "Zolder 1982 · Gilles Villeneuve",
        "description": "Qualifying em Zolder. Villeneuve morre em uma batida terrível após atrito com Pironi em Imola. E se ele tivesse sobrevivido?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Ferrari perde seu ídolo.", "effects": [
                {"type": "remove_driver_from", "driver": "Gilles Villeneuve", "from_year": 1982}
            ]},
            {"id": "survives", "label": "Villeneuve sobrevive", "detail": "Continua na Ferrari, briga por títulos até 1986.", "effects": [
                {"type": "team_override", "driver": "Gilles Villeneuve", "team": "Ferrari", "from_year": 1982, "until_year": 1986},
                {"type": "rating_delta", "driver": "Gilles Villeneuve", "delta": 3, "from_year": 1982, "until_year": 1986},
            ]},
        ],
    },
    1993: {
        "id": "prost_1993",
        "title": "Fim de 1993 · Aposentadoria de Alain Prost",
        "description": "Prost anuncia aposentadoria após o tetra em 1993 (parte por conflito com a chegada anunciada de Senna). E se ele tivesse ficado?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Prost se aposenta como tetracampeão.", "effects": [
                {"type": "remove_driver_from", "driver": "Alain Prost", "from_year": 1994}
            ]},
            {"id": "stays", "label": "Prost continua na Williams", "detail": "Duelo Senna × Prost dentro da mesma equipe em 1994. Explosivo.", "effects": [
                {"type": "team_override", "driver": "Alain Prost", "team": "Williams", "from_year": 1994, "until_year": 1995},
                {"type": "rating_delta", "driver": "Alain Prost", "delta": 1, "from_year": 1994, "until_year": 1995},
            ]},
        ],
    },
    1994: {
        "id": "senna_1994",
        "title": "Imola 1994 · Ayrton Senna",
        "description": "1º de maio. Curva Tamburello. Senna morre no GP de San Marino. E se ele tivesse sobrevivido?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Senna morre em Imola. Schumacher assume a era.", "effects": [
                {"type": "remove_driver_from", "driver": "Ayrton Senna", "from_year": 1995}
            ]},
            {"id": "survives_ferrari", "label": "Senna sobrevive → vai à Ferrari em 96", "detail": "Senna termina 1994/95 na Williams e migra pra Ferrari em 1996 (Schumacher fica na Benetton mais tempo).", "effects": [
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Williams", "from_year": 1994, "until_year": 1995},
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Ferrari", "from_year": 1996, "until_year": 2001},
                {"type": "rating_delta", "driver": "Ayrton Senna", "delta": 2, "from_year": 1994, "until_year": 2001},
                {"type": "team_override", "driver": "Michael Schumacher", "team": "Benetton", "from_year": 1996, "until_year": 1998},
            ]},
            {"id": "survives_stays", "label": "Senna sobrevive → fica na Williams", "detail": "Senna e a Williams dominam os anos 90.", "effects": [
                {"type": "team_override", "driver": "Ayrton Senna", "team": "Williams", "from_year": 1994, "until_year": 2000},
                {"type": "rating_delta", "driver": "Ayrton Senna", "delta": 2, "from_year": 1994, "until_year": 2000},
            ]},
        ],
    },
    2006: {
        "id": "schumi_2006",
        "title": "Fim de 2006 · Aposentadoria de Schumacher",
        "description": "Schumacher se aposenta após 2006. E se ele tivesse ficado na Ferrari por mais alguns anos?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Kimi Raikkonen assume a Ferrari em 2007.", "effects": [
                {"type": "remove_driver_from", "driver": "Michael Schumacher", "from_year": 2007}
            ]},
            {"id": "stays", "label": "Schumi fica até 2009", "detail": "Ferrari mantém o alemão e Raikkonen vai para outra equipe.", "effects": [
                {"type": "team_override", "driver": "Michael Schumacher", "team": "Ferrari", "from_year": 2007, "until_year": 2009},
                {"type": "rating_delta", "driver": "Michael Schumacher", "delta": 1, "from_year": 2007, "until_year": 2009},
            ]},
        ],
    },
    2008: {
        "id": "singapore_gate",
        "title": "Cingapura 2008 · Crashgate",
        "description": "Piquet Jr. bate propositalmente para Alonso vencer. E se a Renault não tivesse armado o esquema?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Alonso vence com auxílio do crash forjado.", "effects": []},
            {"id": "clean", "label": "Renault joga limpo", "detail": "Massa vence em Cingapura e chega ao final do ano com vantagem maior sobre Hamilton.", "effects": [
                {"type": "rating_delta", "driver": "Felipe Massa", "delta": 3, "from_year": 2008, "until_year": 2008},
                {"type": "rating_delta", "driver": "Fernando Alonso", "delta": -2, "from_year": 2008, "until_year": 2008},
            ]},
        ],
    },
    2014: {
        "id": "alonso_ferrari_2014",
        "title": "Fim de 2014 · Alonso deixa a Ferrari?",
        "description": "Alonso trocou a Ferrari pela McLaren-Honda em 2015 — desastre. E se ele tivesse ficado em Maranello?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Alonso vai para McLaren-Honda. Vettel vai à Ferrari.", "effects": []},
            {"id": "stays", "label": "Alonso fica na Ferrari", "detail": "Vettel fica na Red Bull, Alonso disputa com Hamilton.", "effects": [
                {"type": "team_override", "driver": "Fernando Alonso", "team": "Ferrari", "from_year": 2015, "until_year": 2018},
                {"type": "rating_delta", "driver": "Fernando Alonso", "delta": 2, "from_year": 2015, "until_year": 2018},
            ]},
        ],
    },
    2016: {
        "id": "rosberg_2016",
        "title": "Fim de 2016 · Rosberg se aposenta",
        "description": "Dias depois de ganhar o mundial, Rosberg anuncia aposentadoria. E se ele tivesse continuado na Mercedes?",
        "choices": [
            {"id": "real", "label": "Aconteceu como na história", "detail": "Bottas assume a Mercedes.", "effects": [
                {"type": "remove_driver_from", "driver": "Nico Rosberg", "from_year": 2017}
            ]},
            {"id": "stays", "label": "Rosberg continua até 2020", "detail": "Duelo Hamilton × Rosberg segue rendendo.", "effects": [
                {"type": "team_override", "driver": "Nico Rosberg", "team": "Mercedes", "from_year": 2017, "until_year": 2020},
                {"type": "rating_delta", "driver": "Nico Rosberg", "delta": 1, "from_year": 2017, "until_year": 2020},
            ]},
        ],
    },
}


def event_for_year(year: int, resolved_ids: list[str]) -> dict | None:
    ev = EVENTS.get(year)
    if not ev:
        return None
    if ev["id"] in resolved_ids:
        return None
    return ev


def apply_effects(drivers: list[dict], year: int, effects: list[dict]) -> list[dict]:
    """Return a NEW roster after applying effects (adds missing drivers as needed)."""
    roster = {d["name"]: dict(d) for d in drivers}
    # Track default ratings from any effect that added them + fallback
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
                roster[name] = {
                    "name": name,
                    "team": eff["team"],
                    "rating": eff.get("rating", 92),
                }
        elif t == "rating_delta" and name in roster:
            roster[name]["rating"] = max(50, min(99, roster[name]["rating"] + eff["delta"]))
    return list(roster.values())
