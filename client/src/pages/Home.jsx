import { useState } from "react";
import Navbar from "../components/Navbar";
import InputBar from "../components/InputBar";
import Loader from "../components/Loader";
import MovieCard from "../components/MovieCard";
import api from "../utils/api";

export default function Home() {
    const [movies, setMovies] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    const handleSearch = async (mood) => {
        if (!mood.trim()) return alert("Please enter a mood or genre!");

        try {
            setLoading(true);
            setError(null);
            setMovies([]);

            console.log("🎬 Sending request to backend with mood:", mood);

            const response = await api.post("/recommend", {
                mood_or_genre: mood,
                simulate_delay: false,
            });

            if (response?.data?.movies?.length > 0) {
                setMovies(response.data.movies);
            } else {
                setError("No movie recommendations found for that mood 😢");
            }
        } catch (err) {
            console.error("❌ Error fetching movies:", err);
            setError("Something went wrong while fetching recommendations.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen bg-gradient-to-b from-gray-900 to-gray-950 text-white">
            <Navbar />

            <main className="max-w-6xl mx-auto px-4 py-8">
                <div className="mb-6">
                    <InputBar onSubmit={handleSearch} />
                </div>

                {loading && <Loader />}

                {error && (
                    <div className="text-red-400 text-center mt-6 animate-pulse">
                        {error}
                    </div>
                )}

                {!loading && !error && movies.length > 0 && (
                    <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6 mt-6">
                        {movies.map((movie) => (
                            <MovieCard key={movie.imdb_id || movie.title} movie={movie} />
                        ))}
                    </div>
                )}

                {!loading && !error && movies.length === 0 && (
                    <div className="text-gray-400 mt-6 text-center">
                        Enter a mood or genre and press <b>Search</b> to get movie
                        recommendations.
                    </div>
                )}
            </main>
        </div>
    );
}
