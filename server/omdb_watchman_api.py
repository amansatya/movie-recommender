import os
import httpx
import asyncio
from dotenv import load_dotenv
from googleapiclient.discovery import build

load_dotenv()

OMDB_API_KEY = os.getenv("OMDB_API_KEY")
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
WATCHMODE_API_KEY = os.getenv("WATCHMODE_API_KEY")

youtube = build("youtube", "v3", developerKey=YOUTUBE_API_KEY)

async def fetch_ott_from_watchmode(client: httpx.AsyncClient, imdb_id: str, title: str = None):

    if not WATCHMODE_API_KEY:
        print("Warning: WATCHMODE_API_KEY not found in .env file")
        return []

    try:
        search_url = "https://api.watchmode.com/v1/search/"
        params = {
            "apiKey": WATCHMODE_API_KEY,
            "search_field": "imdb_id",
            "search_value": imdb_id
        }
        resp = await client.get(search_url, params=params, timeout=10.0)
        resp.raise_for_status()
        search_results = resp.json().get("title_results", [])
        if not search_results:
            return []

        watchmode_id = search_results[0]["id"]

        details_url = f"https://api.watchmode.com/v1/title/{watchmode_id}/details/"
        params = {"apiKey": WATCHMODE_API_KEY, "append_to_response": "sources"}
        resp = await client.get(details_url, params=params, timeout=10.0)
        resp.raise_for_status()
        data = resp.json()

        sources = data.get("sources", [])
        ott_platforms = set()
        for source in sources:
            if source.get("region") == "IN" and source.get("type") in ["sub", "free"]:
                name = source.get("name")
                if name:
                    ott_platforms.add(name)

        return list(ott_platforms)

    except Exception as e:
        print(f"Error fetching Watchmode data for {title or imdb_id}: {e}")
        return []

async def fetch_movie_details(client: httpx.AsyncClient, imdb_id: str):
    try:
        url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&i={imdb_id}"
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()

        trailer = None
        try:
            loop = asyncio.get_event_loop()
            items = await loop.run_in_executor(None, lambda: youtube.search().list(
                part="snippet",
                q=f"{data.get('Title', '')} trailer",
                maxResults=1,
                type="video"
            ).execute().get("items", []))
            if items:
                trailer = f"https://www.youtube.com/watch?v={items[0]['id']['videoId']}"
        except Exception as e:
            trailer = None
            print(f"Warning: YouTube trailer not found for {data.get('Title')}: {e}")

        otts = await fetch_ott_from_watchmode(client, imdb_id, data.get("Title"))

        return {
            "title": data.get("Title"),
            "poster": data.get("Poster") if data.get("Poster") != "N/A" else None,
            "release_year": data.get("Year"),
            "genre": data.get("Genre").split(", ") if data.get("Genre") else [],
            "director": data.get("Director"),
            "trailer": trailer,
            "otts": otts,
            "rating": float(data.get("imdbRating", 0)) if data.get("imdbRating") != "N/A" else 0.0,
            "vote_count": int(data.get("imdbVotes", "0").replace(",", "")),
            "overview": data.get("Plot")[:150] + "..." if data.get("Plot") else "N/A"
        }
    except Exception as e:
        print(f"Error fetching OMDb data for {imdb_id}: {e}")
        return None

async def search_movies(query: str, limit: int = 6):
    async with httpx.AsyncClient(timeout=60.0) as client:
        try:
            search_url = f"http://www.omdbapi.com/?apikey={OMDB_API_KEY}&s={query}&type=movie&page=1"
            resp = await client.get(search_url)
            resp.raise_for_status()
            results = resp.json().get("Search", [])[:limit * 3]

            tasks = [fetch_movie_details(client, movie["imdbID"]) for movie in results]
            detailed_movies = await asyncio.gather(*tasks)

            unique_movies = {}
            for m1 in filter(None, detailed_movies):
                title = m1["title"]
                if title not in unique_movies or m1["rating"] > unique_movies[title]["rating"]:
                    unique_movies[title] = m1

            sorted_movies = sorted(unique_movies.values(), key=lambda x: (x["rating"], x["vote_count"]), reverse=True)
            return sorted_movies[:limit]

        except Exception as e:
            print(f"OMDb fetch error: {e}")
            return []

if __name__ == "__main__":
    movies = asyncio.run(search_movies("Action"))
    for i, m in enumerate(movies, 1):
        print(f"Movie {i}")
        print(f"Title: {m['title']}")
        print(f"Year: {m['release_year']}")
        print(f"Genre: {m['genre']}")
        print(f"Director: {m['director']}")
        print(f"OTT Platforms: {m['otts']}")
        print(f"Trailer: {m['trailer']}")
        print(f"Rating: {m['rating']}")
        print(f"Votes: {m['vote_count']}")
        print(f"Plot: {m['overview']}\n")
