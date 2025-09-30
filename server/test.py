# import asyncio
# from omdb_watchman_api import search_movies
#
# async def main():
#     query = "Action"
#     movies = await search_movies(query, limit=5)
#
#     if not movies:
#         print("No movies found!")
#         return
#
#     for i, movie in enumerate(movies, start=1):
#         print(f"\n🎬 Movie {i}")
#         print("Title:", movie.get("title"))
#         print("Year:", movie.get("release_year"))
#         print("Genre:", movie.get("genre"))
#         print("Director:", movie.get("director"))
#         print("OTT Platforms:", movie.get("otts"))
#         print("Trailer:", movie.get("trailer"))
#         print("Rating:", movie.get("rating"))
#         print("Votes:", movie.get("vote_count"))
#         print("Plot:", movie.get("overview"))
#
# if __name__ == "__main__":
#     asyncio.run(main())

# main.py (snippet)
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
