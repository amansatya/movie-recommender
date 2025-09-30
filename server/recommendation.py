import asyncio
from omdb_watchman_api import search_movies   # ✅ Correct import
from gemini_api import get_suggested_genres  # ✅ For mood → refined queries


async def generate_recommendations(user_input: str, max_movies: int = 6, delay_seconds: int = 5):
    """
    Generate movie recommendations based on user input (mood/genre).
    Steps:
    1. Ask Gemini API to refine mood/genre into search-friendly queries.
    2. For each query, fetch movies using OMDb + Utelly + YouTube (via omdb_utelly_api).
    3. Deduplicate + rank results by IMDb rating / votes.
    4. Simulate wait (delay_seconds).
    5. Return top 'max_movies' recommendations.
    """

    # Step 1: Refine queries using Gemini
    refined_queries = get_suggested_genres(user_input)
    print(f"🎯 Refined queries from Gemini: {refined_queries}")

    if not refined_queries:
        refined_queries = [user_input]

    # Step 2: Fetch movies from OMDb + Utelly for each refined query
    all_movies = []
    movies_per_genre = max(1, max_movies // len(refined_queries))

    for query in refined_queries:
        print(f"🔎 Searching for: {query}")
        attempts = 0
        while attempts < 2:  # retry up to 2 times
            try:
                movies = await search_movies(query, limit=movies_per_genre + 2)
                all_movies.extend(movies)
                break
            except Exception as e:
                print(f"⚠️ Warning: failed fetching '{query}' attempt {attempts + 1}: {e}")
                attempts += 1
                await asyncio.sleep(0.5)

    # Step 3: Deduplicate movies (keep highest rated version)
    unique_movies_dict = {}
    for movie in all_movies:
        title = movie.get('title')
        if not title:
            continue
        if (
            title not in unique_movies_dict
            or movie.get('rating', 0) > unique_movies_dict[title].get('rating', 0)
        ):
            unique_movies_dict[title] = movie

    unique_movies = list(unique_movies_dict.values())

    # Step 4: Sort by IMDb rating (then votes if available)
    unique_movies.sort(
        key=lambda x: (x.get('rating', 0), x.get('vote_count', 0)),
        reverse=True
    )

    # Step 5: Simulate delay
    if delay_seconds > 0:
        print(f"⏳ Simulating wait for {delay_seconds} seconds...")
        await asyncio.sleep(delay_seconds)

    # Step 6: Take top N movies
    final_movies = unique_movies[:max_movies]
    print(f"✅ Returning {len(final_movies)} movies")

    return final_movies
