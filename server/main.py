from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import asyncio
import logging
from recommendation import generate_recommendations

# -------------------------
# Logging Setup
# -------------------------
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger(__name__)

# -------------------------
# FastAPI App
# -------------------------
app = FastAPI(
    title="Movie Recommender API",
    version="1.0",
    description="Backend API for Movie Recommender (Gemini + OMDb + Utelly + YouTube)"
)

# -------------------------
# CORS Setup (frontend allowed)
# -------------------------
origins = [
    "http://localhost:5173",  # Vite default (frontend dev)
    "http://localhost:3000",  # CRA default
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# Request Model
# -------------------------
class UserInput(BaseModel):
    mood_or_genre: str
    simulate_delay: bool = False  # For testing (true = wait 2 mins)


# -------------------------
# Health Check
# -------------------------
@app.get("/ping")
async def ping():
    return {"message": "pong"}


# -------------------------
# Recommendation Endpoint
# -------------------------
@app.post("/recommend")
async def recommend_movies_endpoint(user_input: UserInput):
    try:
        logger.info(f"🎬 Received request for mood/genre: {user_input.mood_or_genre}")

        # Step 1: Optional artificial delay (only when testing simulate_delay = True)
        if user_input.simulate_delay:
            logger.info("⏳ Simulating 2-minute delay before recommendations...")
            await asyncio.sleep(120)

        # Step 2: Generate recommendations
        movies = await generate_recommendations(user_input.mood_or_genre, max_movies=6)

        # Step 3: Handle empty results
        if not movies:
            logger.warning("⚠️ No movies found for this query.")
            return {"message": "No movies found for your input."}

        logger.info(f"✅ Returning {len(movies)} movies")
        return {"movies": movies}

    except Exception as e:
        logger.error(f"💥 Error in recommendation endpoint: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------
# Run Server (Dev Mode)
# -------------------------
if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Starting FastAPI server at http://127.0.0.1:8000/ping")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
