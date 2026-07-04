"""F1 season simulator - race-by-race stateful engine.

State document shape:
{
  id, year, seed, created_at,
  drivers: [{name, team, rating}],
  circuits: [str, ...],
  points_scheme: [int, ...],  # points awarded per finishing position
  current_race: int,  # index of the NEXT race to run (0 == none run yet)
  total_races: int,
  races: [ { round, circuit, podium: [...], results: [...] }, ... ],
  driver_points: { name: int },
  driver_wins: { name: int },
  driver_podiums: { name: int },
  team_points: { team: int },
  finished: bool,
  news: [ ... ]   # populated when finished
}
"""
import random
from f1_data import get_season, get_circuits_for_year


def points_scheme(year: int) -> list[int]:
    """Historical F1 points system for the given year (simplified)."""
    if 1950 <= year <= 1959:
        return [8, 6, 4, 3, 2]
    if year == 1960:
        return [8, 6, 4, 3, 2, 1]
    if 1961 <= year <= 1990:
        return [9, 6, 4, 3, 2, 1]
    if 1991 <= year <= 2002:
        return [10, 6, 4, 3, 2, 1]
    if 2003 <= year <= 2009:
        return [10, 8, 6, 5, 4, 3, 2, 1]
    return [25, 18, 15, 12, 10, 8, 6, 4, 2, 1]  # 2010+


def create_initial_state(year: int, seed: int) -> dict | None:
    season = get_season(year)
    if not season:
        return None
    circuits = get_circuits_for_year(year, season["num_races"])
    drivers = [
        {"name": n, "team": t, "rating": r} for n, t, r in season["drivers"]
    ]
    return {
        "year": year,
        "seed": seed,
        "drivers": drivers,
        "circuits": circuits,
        "points_scheme": points_scheme(year),
        "current_race": 0,
        "total_races": len(circuits),
        "races": [],
        "driver_points": {d["name"]: 0 for d in drivers},
        "driver_wins": {d["name"]: 0 for d in drivers},
        "driver_podiums": {d["name"]: 0 for d in drivers},
        "team_points": {},
        "finished": False,
        "news": [],
    }


def simulate_next_race(state: dict) -> dict:
    """Advance the state by one race. Idempotent-ish: does nothing if finished."""
    if state["finished"] or state["current_race"] >= state["total_races"]:
        state["finished"] = True
        return state

    # Deterministic-per-race RNG derived from seed + race index
    rng = random.Random((state["seed"] or 0) * 10007 + state["current_race"] + 1)
    round_idx = state["current_race"] + 1
    circuit = state["circuits"][state["current_race"]]
    drivers = state["drivers"]
    pts_scheme = state["points_scheme"]

    scored = []
    for d in drivers:
        noise = rng.gauss(0, 8)
        luck = rng.uniform(-6, 6)
        dnf_roll = rng.random()
        if dnf_roll < 0.05:
            score = -1000  # DNF
        else:
            score = d["rating"] + noise + luck
        scored.append((score, d["name"], d["team"]))
    scored.sort(reverse=True, key=lambda x: x[0])

    podium = []
    results = []
    for pos, (sc, name, team) in enumerate(scored):
        finished_race = sc > -1000
        pts = 0
        if finished_race and pos < len(pts_scheme):
            pts = pts_scheme[pos]
            state["driver_points"][name] = state["driver_points"].get(name, 0) + pts
            state["team_points"][team] = state["team_points"].get(team, 0) + pts
        if finished_race and pos < 3:
            state["driver_podiums"][name] = state["driver_podiums"].get(name, 0) + 1
            podium.append({"position": pos + 1, "driver": name, "team": team})
        if finished_race and pos == 0:
            state["driver_wins"][name] = state["driver_wins"].get(name, 0) + 1
        results.append({
            "position": pos + 1 if finished_race else None,
            "driver": name,
            "team": team,
            "dnf": not finished_race,
            "points": pts,
        })

    state["races"].append({
        "round": round_idx,
        "circuit": circuit,
        "podium": podium,
        "results": results,  # ALL drivers, not just top 10
        "standings_snapshot": _snapshot_standings(state),
        "news": None,  # populated by server after Gemini call
    })
    state["current_race"] = round_idx
    if state["current_race"] >= state["total_races"]:
        state["finished"] = True
    return state


def _snapshot_standings(state: dict) -> dict:
    """Snapshot of ALL drivers + constructors after the current race."""
    drivers_by_name = {d["name"]: d for d in state["drivers"]}
    drivers = [
        {
            "driver": name,
            "team": drivers_by_name[name]["team"],
            "points": pts,
            "wins": state["driver_wins"].get(name, 0),
        }
        for name, pts in state["driver_points"].items()
    ]
    drivers.sort(key=lambda x: (-x["points"], -x["wins"]))
    constructors = [
        {"team": t, "points": p}
        for t, p in sorted(state["team_points"].items(), key=lambda kv: -kv[1])
    ]
    return {"drivers": drivers, "constructors": constructors}


def simulate_all_remaining(state: dict) -> dict:
    while not state["finished"]:
        simulate_next_race(state)
    return state


def build_standings(state: dict) -> dict:
    """Compute driver + constructor standings on demand."""
    drivers_by_name = {d["name"]: d for d in state["drivers"]}
    driver_standings = []
    for name, pts in state["driver_points"].items():
        driver_standings.append({
            "driver": name,
            "team": drivers_by_name[name]["team"],
            "points": pts,
            "wins": state["driver_wins"].get(name, 0),
            "podiums": state["driver_podiums"].get(name, 0),
        })
    driver_standings.sort(key=lambda x: (-x["points"], -x["wins"], -x["podiums"]))

    constructor_standings = [
        {"team": t, "points": p}
        for t, p in sorted(state["team_points"].items(), key=lambda kv: -kv[1])
    ]
    return {
        "driver_standings": driver_standings,
        "constructor_standings": constructor_standings,
    }


def build_summary(state: dict) -> dict:
    """Snapshot summary used by both the UI and news generator."""
    season = get_season(state["year"])
    standings = build_standings(state)
    ds = standings["driver_standings"]
    cs = standings["constructor_standings"]
    champion = ds[0] if ds and state["finished"] else None
    return {
        "year": state["year"],
        "champion": champion,
        "runner_up": ds[1] if len(ds) > 1 and state["finished"] else None,
        "constructor_champion": cs[0] if cs and state["finished"] else None,
        "real_champion": {"driver": season["champion"], "team": season["champion_team"]},
        "real_constructor_champion": season["constructors_champion"],
        "upset": bool(champion and champion["driver"] != season["champion"]),
        "num_races": state["total_races"],
        "races_completed": state["current_race"],
        "finished": state["finished"],
    }
