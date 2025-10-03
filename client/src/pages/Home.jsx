import { useState } from "react";
import Navbar from "../components/Navbar";
import InputBar from "../components/InputBar";
import Loader from "../components/Loader";
import MovieCard from "../components/MovieCard";

/* Mock data to test MovieCard layout quickly */
const mockMovies = [
    {
        imdb_id: "tt0111161",
        title: "The Shawshank Redemption",
        year: "1994",
        director: "Frank Darabont",
        genre: "Drama",
        poster: "https://upload.wikimedia.org/wikipedia/en/8/81/ShawshankRedemptionMoviePoster.jpg",
        imdb_rating: "9.3",
        plot: "Two imprisoned men bond over a number of years...",
        ott_platforms: ["Netflix", "Prime Video"],
        trailer: "https://www.youtube.com/watch?v=NmzuHjWmXOc"
    },
    // ... add up to 6 mock items if you like
];

export default function Home() {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);

    const handleSearch = async (mood) => {
        setLoading(true);
        setMovies([]);
        // simulate backend processing time (2s here — replace with real fetch)
        await new Promise((r) => setTimeout(r, 2000));
        // for now, return mock data
        setMovies(mockMovies);
        setLoading(false);
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-950 text-white">
            <Navbar />
            <main className="max-w-6xl mx-auto px-4 py-8">
                <div className="mb-6">
                    <InputBar onSubmit={handleSearch} />
                </div>

                {loading ? (
                    <Loader />
                ) : movies.length > 0 ? (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                        {movies.map((m) => (
                            <MovieCard key={m.imdb_id || m.title} movie={m} />
                        ))}
                    </div>
                ) : (
                    <div className="text-gray-400 mt-6">Enter a mood or genre and press Search to get recommendations.</div>
                )}
            </main>
        </div>
    );
}
