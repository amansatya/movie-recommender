import asyncio
from omdb_watchman_api import search_movies
from gemini_api import get_suggested_genres


async def generate_recommendations(user_input: str, max_movies: int = 6, delay_seconds: int = 5):

    refined_queries = get_suggested_genres(user_input)
    print(f"Refined queries from Gemini: {refined_queries}")

    if not refined_queries:
        refined_queries = [user_input]

    all_movies = []
    movies_per_genre = max(1, max_movies // len(refined_queries))

    for query in refined_queries:
        print(f"Searching for: {query}")
        attempts = 0
        while attempts < 2:
            try:
                movies = await search_movies(query, limit=movies_per_genre + 2)
                all_movies.extend(movies)
                break
            except Exception as e:
                print(f"Warning: failed fetching '{query}' attempt {attempts + 1}: {e}")
                attempts += 1
                await asyncio.sleep(0.5)

    unique_movies_dict = {}
    for movie in all_movies:
        title = movie['title']
        if title not in unique_movies_dict or movie.get('rating', 0) > unique_movies_dict[title].get('rating', 0):
            unique_movies_dict[title] = movie

    unique_movies = list(unique_movies_dict.values())
    unique_movies.sort(key=lambda x: (x.get('rating', 0), x.get('vote_count', 0)), reverse=True)

    if delay_seconds > 0:
        print(f"Simulating wait for {delay_seconds} seconds...")
        await asyncio.sleep(delay_seconds)

    final_movies = unique_movies[:max_movies]
    print(f"Returning {len(final_movies)} movies")
    return final_movies
