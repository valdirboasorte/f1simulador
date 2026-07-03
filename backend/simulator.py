"""F1 season simulator engine."""
import random
from collections import defaultdict
from f1_data import get_season, get_circuits_for_year

POINTS = [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]


def simulate_season(year: int, seed: int | None = None):
    """Simulate an alternate reality of a real F1 season.
    Returns a dict with races, driver_standings, constructor_standings, summary.
    """
    season = get_season(year)
    if not season:
        return None

    rng = random.Random(seed)
    drivers = season["drivers"]
    circuits = get_circuits_for_year(year, season["num_races"])

    driver_points = defaultdict(int)
    driver_team = {d[0]: d[1] for d in drivers}
    driver_wins = defaultdict(int)
    driver_podiums = defaultdict(int)
    team_points = defaultdict(int)

    races = []
    for idx, circuit in enumerate(circuits, start=1):
        # Score each driver for this race
        scored = []
        for name, team, rating in drivers:
            # rating + gaussian noise + occasional random luck spike/DNF
            noise = rng.gauss(0, 8)
            luck = rng.uniform(-6, 6)
            dnf_roll = rng.random()
            if dnf_roll < 0.05:  # ~5% DNF chance
                score = -1000
            else:
                score = rating + noise + luck
            scored.append((score, name, team))
        scored.sort(reverse=True, key=lambda x: x[0])

        # Assign points to top 10 finishers
        podium = []
        result = []
        for pos, (sc, name, team) in enumerate(scored):
            finished = sc > -1000
            entry = {
                "position": pos + 1 if finished else None,
                "driver": name,
                "team": team,
                "dnf": not finished,
            }
            result.append(entry)
            if finished and pos < 10:
                pts = POINTS[pos]
                driver_points[name] += pts
                team_points[team] += pts
                entry["points"] = pts
            else:
                entry["points"] = 0
            if finished and pos < 3:
                driver_podiums[name] += 1
                podium.append({"position": pos + 1, "driver": name, "team": team})
            if finished and pos == 0:
                driver_wins[name] += 1

        races.append({
            "round": idx,
            "circuit": circuit,
            "podium": podium,
            "results": result[:10],  # only top 10 to keep payload small
        })

    # Build standings
    driver_standings = []
    for name in driver_points:
        driver_standings.append({
            "driver": name,
            "team": driver_team[name],
            "points": driver_points[name],
            "wins": driver_wins[name],
            "podiums": driver_podiums[name],
        })
    driver_standings.sort(key=lambda x: (-x["points"], -x["wins"]))

    constructor_standings = [
        {"team": team, "points": pts}
        for team, pts in sorted(team_points.items(), key=lambda kv: -kv[1])
    ]

    champion = driver_standings[0] if driver_standings else None
    real_champion = {"driver": season["champion"], "team": season["champion_team"]}
    real_constructor = season["constructors_champion"]

    summary = {
        "year": year,
        "champion": champion,
        "runner_up": driver_standings[1] if len(driver_standings) > 1 else None,
        "constructor_champion": constructor_standings[0] if constructor_standings else None,
        "real_champion": real_champion,
        "real_constructor_champion": real_constructor,
        "upset": champion and champion["driver"] != real_champion["driver"],
        "num_races": len(races),
    }

    return {
        "year": year,
        "seed": seed,
        "summary": summary,
        "races": races,
        "driver_standings": driver_standings,
        "constructor_standings": constructor_standings,
    }
