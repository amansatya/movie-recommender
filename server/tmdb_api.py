import os
import httpx
import asyncio
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = "https://api.themoviedb.org/3"

GENRE_IDS = {
    'Action': 28, 'Adventure': 12, 'Animation': 16, 'Comedy': 35, 'Crime': 80,
    'Documentary': 99, 'Drama': 18, 'Family': 10751, 'Fantasy': 14, 'History': 36,
    'Horror': 27, 'Music': 10402, 'Mystery': 9648, 'Romance': 10749, 'Science Fiction': 878,
    'TV Movie': 10770, 'Thriller': 53, 'War': 10752, 'Western': 37, 'Sci-Fi': 878
}

async def fetch_movie_details(client: httpx.AsyncClient, movie, current_year):
    try:
        movie_id = movie["id"]
        url = f"{BASE_URL}/movie/{movie_id}?api_key={TMDB_API_KEY}&append_to_response=videos,watch/providers,credits"
        resp = await client.get(url)
        resp.raise_for_status()
        details = resp.json()

        director = next(
            (crew["name"] for crew in details.get("credits", {}).get("crew", []) if crew["job"] == "Director"),
            "N/A"
        )
        trailer = next(
            (f"https://www.youtube.com/watch?v={v['key']}" for v in details.get("videos", {}).get("results", [])
             if v["type"] == "Trailer" and v["site"] == "YouTube"),
            None
        )

        watch_providers = details.get("watch/providers", {}).get("results", {}).get("IN", {})
        otts = []
        for provider_type in ["flatrate", "rent", "buy"]:
            if provider_type in watch_providers:
                otts.extend([ott["provider_name"] for ott in watch_providers[provider_type]])
        otts = list(set([ott.replace("Amazon Prime Video with Ads", "Prime Video") for ott in otts]))

        release_year = details.get("release_date", "")[:4] if details.get("release_date") else "N/A"
        vote_avg = round(details.get("vote_average", 0), 1)
        vote_count = details.get("vote_count", 0)

        if vote_avg >= 6.0 and vote_count >= 100:
            return {
                "title": details.get("title"),
                "poster": f"https://image.tmdb.org/t/p/w500{details.get('poster_path')}" if details.get("poster_path") else None,
                "release_year": release_year,
                "genre": [g["name"] for g in details.get("genres", [])],
                "director": director,
                "trailer": trailer,
                "otts": otts,
                "rating": vote_avg,
                "vote_count": vote_count,
                "overview": (details.get("overview", "")[:150] + "...") if details.get("overview") else "N/A"
            }
    except Exception as e:
        print(f"Error processing movie {movie.get('title', 'Unknown')}: {e}")
        return None

async def search_movies(query: str, limit: int = 6):
    current_year = datetime.now().year
    async with httpx.AsyncClient(timeout=45.0) as client:
        try:
            genre_id = GENRE_IDS.get(query.title())
            if genre_id:
                discover_url = f"{BASE_URL}/discover/movie?api_key={TMDB_API_KEY}&with_genres={genre_id}&sort_by=popularity.desc&vote_count.gte=300&vote_average.gte=6.5&include_adult=false&primary_release_date.lte={current_year}-01-01&page=1"
                response = await client.get(discover_url)
            else:
                search_url = f"{BASE_URL}/search/movie?api_key={TMDB_API_KEY}&query={query}&include_adult=false&page=1"
                response = await client.get(search_url)

            response.raise_for_status()
            results = response.json().get("results", [])[:limit*3]

            tasks = [fetch_movie_details(client, m, current_year) for m in results]
            detailed_movies = await asyncio.gather(*tasks)

            unique_movies = {}
            for m in filter(None, detailed_movies):
                title = m["title"]
                if title not in unique_movies or m["rating"] > unique_movies[title]["rating"]:
                    unique_movies[title] = m

            sorted_movies = sorted(unique_movies.values(), key=lambda x: (x["rating"], x["vote_count"]), reverse=True)
            return sorted_movies[:limit]

        except Exception as e:
            print(f"TMDB fetch error: {e}")
            return []
