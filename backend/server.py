from fastapi import FastAPI, APIRouter, HTTPException
from dotenv import load_dotenv
from starlette.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import os
import logging
import random
import uuid
from pathlib import Path
from pydantic import BaseModel
from typing import Optional
from datetime import datetime, timezone

ROOT_DIR = Path(__file__).parent
load_dotenv(ROOT_DIR / '.env')

from f1_data import SEASONS, get_all_years, get_season
from simulator import (
    create_initial_state,
    simulate_next_race,
    simulate_all_remaining,
    build_standings,
    build_summary,
)
from news_generator import generate_news, generate_race_news
from whatif_events import event_for_year, apply_effects, EVENTS as WHATIF_EVENTS

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="F1 Alt Reality Simulator")
api_router = APIRouter(prefix="/api")


class SimulateRequest(BaseModel):
    year: int
    seed: Optional[int] = None
    reality_id: Optional[str] = None


class CreateRealityRequest(BaseModel):
    name: str = "Minha Realidade"


def _serialize(state: dict) -> dict:
    """Attach computed views for the client."""
    standings = build_standings(state)
    return {
        **state,
        "summary": build_summary(state),
        "driver_standings": standings["driver_standings"],
        "constructor_standings": standings["constructor_standings"],
    }


async def _load_state(sim_id: str) -> dict:
    doc = await db.simulations.find_one({"id": sim_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return doc


async def _save_state(state: dict):
    await db.simulations.replace_one({"id": state["id"]}, state, upsert=True)


@api_router.get("/")
async def root():
    return {"message": "F1 Alt Reality Simulator API", "seasons": len(SEASONS)}


@api_router.get("/seasons")
async def list_seasons():
    years = get_all_years()
    return [
        {
            "year": y,
            "champion": SEASONS[y]["champion"],
            "champion_team": SEASONS[y]["champion_team"],
            "constructors_champion": SEASONS[y]["constructors_champion"],
            "num_races": SEASONS[y]["num_races"],
        }
        for y in years
    ]


@api_router.get("/seasons/{year}")
async def season_detail(year: int):
    season = get_season(year)
    if not season:
        raise HTTPException(status_code=404, detail="Season not found")
    return {
        "year": year,
        "champion": season["champion"],
        "champion_team": season["champion_team"],
        "constructors_champion": season["constructors_champion"],
        "num_races": season["num_races"],
        "drivers": [
            {"name": n, "team": t, "rating": r} for n, t, r in season["drivers"]
        ],
    }


@api_router.post("/simulate")
async def create_simulation(req: SimulateRequest):
    """Create a new simulation but do NOT run any race yet."""
    if req.year not in SEASONS:
        raise HTTPException(status_code=404, detail="Season not found")
    seed = req.seed if req.seed is not None else random.randint(1, 10**9)
    state = create_initial_state(req.year, seed)
    if not state:
        raise HTTPException(status_code=500, detail="Failed to init simulation")

    # If linked to a reality, apply cumulative what-if effects to the roster
    if req.reality_id:
        reality = await db.realities.find_one({"id": req.reality_id}, {"_id": 0})
        if not reality:
            raise HTTPException(status_code=404, detail="Reality not found")
        # Block simulate if there's a pending event
        pending = event_for_year(req.year, [e["event_id"] for e in reality.get("resolved_events", [])])
        if pending:
            raise HTTPException(status_code=400, detail=f"Resolve event first: {pending['id']}")
        effects = reality.get("applied_effects", [])
        modified = apply_effects(state["drivers"], req.year, effects)
        if not modified:
            raise HTTPException(status_code=400, detail="All drivers removed by effects")
        state["drivers"] = modified
        # Rebuild point/win/podium bookkeeping dicts to match new roster
        state["driver_points"] = {d["name"]: 0 for d in modified}
        state["driver_wins"] = {d["name"]: 0 for d in modified}
        state["driver_podiums"] = {d["name"]: 0 for d in modified}

    state["id"] = str(uuid.uuid4())
    state["created_at"] = datetime.now(timezone.utc).isoformat()
    state["reality_id"] = req.reality_id
    await _save_state(state)
    return _serialize(state)


@api_router.get("/simulations/{sim_id}")
async def get_simulation(sim_id: str):
    state = await _load_state(sim_id)
    return _serialize(state)


@api_router.post("/simulations/{sim_id}/next")
async def next_race(sim_id: str):
    state = await _load_state(sim_id)
    if state["finished"]:
        return _serialize(state)
    simulate_next_race(state)
    # Auto-generate news for the race we just ran
    last_race = state["races"][-1]
    news = await generate_race_news(state, last_race)
    last_race["news"] = news
    await _save_state(state)
    return _serialize(state)


@api_router.post("/simulations/{sim_id}/finish")
async def finish_all(sim_id: str):
    """Simulate all remaining races. News is generated only for the FINAL race
    to avoid a very long request. Individual per-race news for skipped rounds
    can be generated later via /race/{round}/news if needed."""
    state = await _load_state(sim_id)
    simulate_all_remaining(state)
    if state["races"]:
        last = state["races"][-1]
        if not last.get("news"):
            last["news"] = await generate_race_news(state, last)
    await _save_state(state)
    return _serialize(state)


@api_router.post("/simulations/{sim_id}/race/{round_num}/news")
async def make_race_news(sim_id: str, round_num: int):
    """Generate news for a specific race if it's missing."""
    state = await _load_state(sim_id)
    target = next((r for r in state["races"] if r["round"] == round_num), None)
    if not target:
        raise HTTPException(status_code=404, detail="Race not found")
    if target.get("news"):
        return {"news": target["news"]}
    target["news"] = await generate_race_news(state, target)
    await _save_state(state)
    return {"news": target["news"]}


@api_router.post("/simulations/{sim_id}/news")
async def make_news(sim_id: str):
    state = await _load_state(sim_id)
    if not state["finished"]:
        raise HTTPException(status_code=400, detail="Season is not finished yet")
    if state.get("news"):
        return {"news": state["news"]}
    # Build shape expected by generator
    payload = {
        "summary": build_summary(state),
        "races": state["races"],
        "driver_standings": build_standings(state)["driver_standings"],
        "year": state["year"],
        "seed": state["seed"],
    }
    news = await generate_news(payload)
    state["news"] = news
    await _save_state(state)
    return {"news": news}


@api_router.get("/simulations")
async def list_simulations(limit: int = 20):
    cursor = db.simulations.find({}, {"_id": 0, "races": 0}).sort("created_at", -1).limit(limit)
    docs = await cursor.to_list(limit)
    return docs


# ---------- MINHA REALIDADE (chronological career mode) ----------

FIRST_YEAR = min(SEASONS.keys())
LAST_YEAR = max(SEASONS.keys())


def _new_reality(name: str) -> dict:
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "current_year": FIRST_YEAR,
        "driver_stats": {},
        "constructor_stats": {},
        "seasons": [],
        "resolved_events": [],   # [{event_id, year, choice_id, choice_label}]
        "applied_effects": [],   # flat list of effect dicts
        "finished": False,
    }


def _bump(d: dict, key: str, field: str, amount: int = 1):
    if key not in d:
        d[key] = {"wins": 0, "podiums": 0, "championships": 0, "points_career": 0, "teams": []}
    d[key][field] = d[key].get(field, 0) + amount


@api_router.post("/realities")
async def create_reality(req: CreateRealityRequest):
    r = _new_reality(req.name or "Minha Realidade")
    await db.realities.insert_one(r.copy())
    r.pop("_id", None)
    return r


@api_router.get("/realities")
async def list_realities():
    cursor = db.realities.find({}, {"_id": 0}).sort("created_at", -1).limit(50)
    return await cursor.to_list(50)


@api_router.get("/realities/{rid}")
async def get_reality(rid: str):
    doc = await db.realities.find_one({"id": rid}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Reality not found")
    # attach pending event if any
    resolved_ids = [e["event_id"] for e in doc.get("resolved_events", [])]
    doc["pending_event"] = event_for_year(doc["current_year"], resolved_ids)
    return doc


@api_router.post("/realities/{rid}/resolve")
async def resolve_event(rid: str, payload: dict):
    """Body: {year, choice_id}. Applies chosen effects to the reality."""
    reality = await db.realities.find_one({"id": rid}, {"_id": 0})
    if not reality:
        raise HTTPException(status_code=404, detail="Reality not found")
    year = payload.get("year")
    choice_id = payload.get("choice_id")
    if year != reality["current_year"]:
        raise HTTPException(status_code=400, detail="Year mismatch")
    resolved_ids = [e["event_id"] for e in reality.get("resolved_events", [])]
    ev = event_for_year(year, resolved_ids)
    if not ev:
        raise HTTPException(status_code=400, detail="No pending event for this year")
    choice = next((c for c in ev["choices"] if c["id"] == choice_id), None)
    if not choice:
        raise HTTPException(status_code=400, detail="Invalid choice_id")
    reality.setdefault("applied_effects", []).extend(choice.get("effects", []))
    reality.setdefault("resolved_events", []).append({
        "event_id": ev["id"],
        "year": year,
        "choice_id": choice_id,
        "choice_label": choice["label"],
    })
    await db.realities.replace_one({"id": rid}, reality)
    reality["pending_event"] = None
    return reality


@api_router.post("/realities/{rid}/commit/{sim_id}")
async def commit_season(rid: str, sim_id: str):
    """Absorb a finished simulation into the reality timeline and advance year."""
    reality = await db.realities.find_one({"id": rid}, {"_id": 0})
    if not reality:
        raise HTTPException(status_code=404, detail="Reality not found")
    sim = await db.simulations.find_one({"id": sim_id}, {"_id": 0})
    if not sim:
        raise HTTPException(status_code=404, detail="Simulation not found")
    if not sim.get("finished"):
        raise HTTPException(status_code=400, detail="Season not finished")
    year = sim["year"]
    if year != reality["current_year"]:
        raise HTTPException(status_code=400, detail=f"Reality expects year {reality['current_year']}, sim is {year}")
    if any(s["year"] == year for s in reality["seasons"]):
        raise HTTPException(status_code=400, detail="Season already committed")

    ds = reality["driver_stats"]
    cs = reality["constructor_stats"]

    # aggregate per-race wins/podiums + season points
    for race in sim["races"]:
        for p in race.get("podium", []):
            _bump(ds, p["driver"], "podiums")
            _bump(cs, p["team"], "podiums")
            if p["position"] == 1:
                _bump(ds, p["driver"], "wins")
                _bump(cs, p["team"], "wins")
    # career points
    standings = build_standings(sim)
    for d in standings["driver_standings"]:
        _bump(ds, d["driver"], "points_career", d["points"])
        if d["team"] not in ds[d["driver"]]["teams"]:
            ds[d["driver"]]["teams"].append(d["team"])
    for c in standings["constructor_standings"]:
        _bump(cs, c["team"], "points_career", c["points"])

    summary = build_summary(sim)
    if summary["champion"]:
        _bump(ds, summary["champion"]["driver"], "championships")
    if summary["constructor_champion"]:
        _bump(cs, summary["constructor_champion"]["team"], "championships")

    reality["seasons"].append({
        "year": year,
        "sim_id": sim_id,
        "champion": summary["champion"],
        "constructor_champion": summary["constructor_champion"],
        "real_champion": summary["real_champion"]["driver"],
        "upset": summary["upset"],
    })
    if year >= LAST_YEAR:
        reality["finished"] = True
    else:
        reality["current_year"] = year + 1

    await db.realities.replace_one({"id": rid}, reality)
    return reality


app.include_router(api_router)

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_origins=os.environ.get('CORS_ORIGINS', '*').split(','),
    allow_methods=["*"],
    allow_headers=["*"],
)

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@app.on_event("shutdown")
async def shutdown_db_client():
    client.close()
