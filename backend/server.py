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
from simulator import simulate_season
from news_generator import generate_news

mongo_url = os.environ['MONGO_URL']
client = AsyncIOMotorClient(mongo_url)
db = client[os.environ['DB_NAME']]

app = FastAPI(title="F1 Alt Reality Simulator")
api_router = APIRouter(prefix="/api")


class SimulateRequest(BaseModel):
    year: int
    seed: Optional[int] = None


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
async def simulate(req: SimulateRequest):
    if req.year not in SEASONS:
        raise HTTPException(status_code=404, detail="Season not found")
    seed = req.seed if req.seed is not None else random.randint(1, 10**9)
    sim = simulate_season(req.year, seed=seed)
    if not sim:
        raise HTTPException(status_code=500, detail="Simulation failed")

    # Generate news via Gemini
    news = await generate_news(sim)
    sim_id = str(uuid.uuid4())
    doc = {
        "id": sim_id,
        "year": req.year,
        "seed": seed,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "simulation": sim,
        "news": news,
    }
    await db.simulations.insert_one(doc)
    return {
        "id": sim_id,
        "year": req.year,
        "seed": seed,
        "simulation": sim,
        "news": news,
    }


@api_router.get("/simulations/{sim_id}")
async def get_simulation(sim_id: str):
    doc = await db.simulations.find_one({"id": sim_id}, {"_id": 0})
    if not doc:
        raise HTTPException(status_code=404, detail="Simulation not found")
    return doc


@api_router.get("/simulations")
async def list_simulations(limit: int = 20):
    cursor = db.simulations.find({}, {"_id": 0, "simulation.races": 0}).sort("created_at", -1).limit(limit)
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
