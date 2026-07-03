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
from news_generator import generate_news

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="F1 Alt Reality Simulator")
api_router = APIRouter(prefix="/api")


class SimulateRequest(BaseModel):
    year: int
    seed: Optional[int] = None


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
    state["id"] = str(uuid.uuid4())
    state["created_at"] = datetime.now(timezone.utc).isoformat()
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
    await _save_state(state)
    return _serialize(state)


@api_router.post("/simulations/{sim_id}/finish")
async def finish_all(sim_id: str):
    """Simulate all remaining races in one shot."""
    state = await _load_state(sim_id)
    simulate_all_remaining(state)
    await _save_state(state)
    return _serialize(state)


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
