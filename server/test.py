"""Test script to demonstrate the functionality of the tmdb_api module."""

# import asyncio
# from tmdb_api import search_movies
# from tabulate import tabulate
#
# async def main():
#     query = "action"  # Change to any mood/genre
#     movies = await search_movies(query)
#
#     table_data = []
#     for movie in movies:
#         table_data.append([
#             movie['title'],
#             movie['release_year'],
#             ', '.join(movie['genre']) if movie['genre'] else 'N/A',
#             movie['director'],
#             movie['trailer'] if movie['trailer'] else 'N/A',
#             ', '.join(movie['otts']) if movie['otts'] else 'N/A',
#             movie['poster'] if movie['poster'] else 'N/A'
#         ])
#
#     headers = ["Title", "Year", "Genre", "Director", "Trailer", "OTT Platforms", "Poster URL"]
#     print(tabulate(table_data, headers=headers, tablefmt="grid"))
#
# if __name__ == "__main__":
#     asyncio.run(main())



"""Test script to demonstrate the functionality of the gemini_api module."""
# from gemini_api import get_suggested_genres
#
# user_input = "I feel like watching something thrilling and fun"
#
# suggestions = get_suggested_genres(user_input)
#
# print("Suggested genres/themes:", suggestions)


"""Test script for the Movie Recommendation System"""
import asyncio
from recommendation import generate_recommendations


async def test_recommendations():
    test_cases = [
        "happy and adventurous",
        "dark and mysterious",
        "romantic comedy"
    ]

    for test_input in test_cases:
        print(f"\n{'='*70}")
        print(f"Testing movie recommendations for: '{test_input}'")
        print(f"{'='*70}")

        try:
            max_movies = int(input("Enter max number of movies to fetch (default 5): ") or 5)
            movies = await generate_recommendations(test_input, max_movies=max_movies, delay_seconds=5)

            if not movies:
                print("No movies found for this input.")
                continue

            print(f"\nFound {len(movies)} movies:")
            print("-"*70)
            for i, movie in enumerate(movies, 1):
                print(f"\n{i}. {movie['title']} ({movie['release_year']})")
                print(f"   Director: {movie['director']}")
                print(f"   Genres: {', '.join(movie['genre']) if movie['genre'] else 'N/A'}")
                print(f"   Rating: {movie.get('rating', 'N/A')}/10 ({movie.get('vote_count', 0)} votes)")
                print(f"   OTT Platforms: {', '.join(movie['otts']) if movie['otts'] else 'Not available in India'}")
                print(f"   Trailer: {movie.get('trailer') or 'Not available'}")
                print(f"   Poster: {'Available' if movie.get('poster') else 'Not available'}")

        except Exception as e:
            print(f"Error occurred: {e}")

        print(f"\n{'='*70}\n")


async def test_single_recommendation():
    """Simple test for one input"""
    print("Simple test - Happy and adventurous movies")
    print("="*50)
    try:
        max_movies = int(input("Enter max number of movies to fetch (default 5): ") or 5)
        movies = await generate_recommendations("happy and adventurous", max_movies=max_movies, delay_seconds=5)

        for i, movie in enumerate(movies, 1):
            print(f"{i}. {movie['title']} ({movie['release_year']}) - {movie.get('rating', 'N/A')}/10")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    print("Movie Recommendation System Test")
    print("="*50)

    choice = input("Run (1) Simple test or (2) Multiple test cases? Enter 1 or 2: ").strip()

    if choice == "1":
        asyncio.run(test_single_recommendation())
    elif choice == "2":
        asyncio.run(test_recommendations())
    else:
        print("Invalid choice, running simple test by default.")
        asyncio.run(test_single_recommendation())
