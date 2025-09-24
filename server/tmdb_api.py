import os
import httpx
import asyncio
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"


async def search_movies(query: str, limit: int = 6):
    client_configs = [
        {"verify": True, "timeout": 30.0},
        {"verify": False, "timeout": 30.0}
    ]

    for config in client_configs:
        try:
            async with httpx.AsyncClient(**config) as client:
                search_url = f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}"
                response = await client.get(search_url)
                response.raise_for_status()
                data = response.json()
                results = data.get("results", [])[:limit]

                movies = []
                for movie in results:
                    movie_id = movie["id"]
                    details_url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos,watch/providers,credits"
                    detail_resp = await client.get(details_url)
                    detail_resp.raise_for_status()
                    details = detail_resp.json()

                    director = next(
                        (crew["name"] for crew in details.get("credits", {}).get("crew", []) if crew["job"] == "Director"),
                        "N/A"
                    )

                    trailer = next((f"https://www.youtube.com/watch?v={v['key']}"
                                   for v in details.get("videos", {}).get("results", []) if v["type"] == "Trailer"), None)

                    otts = details.get("watch/providers", {}).get("results", {}).get("IN", {}).get("flatrate", [])

                    movies.append({
                        "title": details.get("title"),
                        "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get("poster_path") else None,
                        "release_year": details.get("release_date", "")[:4] if details.get("release_date") else "N/A",
                        "genre": [g["name"] for g in details.get("genres", [])],
                        "director": director,
                        "trailer": trailer,
                        "otts": [ott["provider_name"] for ott in otts] if otts else []
                    })
                    await asyncio.sleep(0.1)

                return movies

        except httpx.ConnectError:
            continue

    raise Exception("Failed to connect to TMDB API. Check internet/firewall settings.")
