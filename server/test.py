from fastapi import FastAPI
import asyncio
from recommendation import generate_recommendations

app = FastAPI()

@app.post("/recommend")
async def recommend(payload: dict):
    user_mood = payload.get("mood", "")
    # simulate 2-minute wait
    await asyncio.sleep(120)
    return await generate_recommendations(user_mood, max_results=6)
