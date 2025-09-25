from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import logging

from recommendation import generate_recommendations

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie Recommender API", version="1.0")

origins = [
    "http://localhost:5173",
    "http://localhost:3000"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

class UserInput(BaseModel):
    mood_or_genre: str
    simulate_delay: bool = False

@app.get("/ping")
async def ping():
    return {"message": "pong"}

@app.post("/recommend")
async def recommend_movies_endpoint(user_input: UserInput):
    try:
        logger.info(f"Received request: {user_input.mood_or_genre}")

        if user_input.simulate_delay:
            logger.info("Simulating 2-minute delay...")
            await asyncio.sleep(120)

        movies = await generate_recommendations(user_input.mood_or_genre)
        if not movies:
            return {"message": "No movies found for your input."}

        logger.info(f"Returning {len(movies)} movies")
        return {"movies": movies}

    except Exception as e:
        logger.error(f"Error in recommendation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting FastAPI server on http://127.0.0.1:8000/ping")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
