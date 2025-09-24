import asyncio
from tmdb_api import search_movies
from tabulate import tabulate

async def main():
    query = "action"  # Change to any mood/genre
    movies = await search_movies(query)

    table_data = []
    for movie in movies:
        table_data.append([
            movie['title'],
            movie['release_year'],
            ', '.join(movie['genre']) if movie['genre'] else 'N/A',
            movie['director'],
            movie['trailer'] if movie['trailer'] else 'N/A',
            ', '.join(movie['otts']) if movie['otts'] else 'N/A',
            movie['poster'] if movie['poster'] else 'N/A'
        ])

    headers = ["Title", "Year", "Genre", "Director", "Trailer", "OTT Platforms", "Poster URL"]
    print(tabulate(table_data, headers=headers, tablefmt="grid"))

if __name__ == "__main__":
    asyncio.run(main())


# from gemini_api import get_suggested_genres
#
# user_input = "I feel like watching something thrilling and fun"
#
# suggestions = get_suggested_genres(user_input)
#
# print("Suggested genres/themes:", suggestions)