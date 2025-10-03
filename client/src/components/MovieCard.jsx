import { useState } from "react";

export default function MovieCard({ movie }) {
    const [isOpen, setIsOpen] = useState(false);

    if (!movie) return null;

    const {
        title,
        year,
        director,
        genre,
        poster,
        imdb_rating,
        plot,
        ott_platforms = [],
        trailer
    } = movie;

    const hasPoster = poster && poster !== "N/A";

    return (
        <>
            {/* Card Preview */}
            <article
                className="bg-white/5 rounded-2xl overflow-hidden shadow-md flex flex-col cursor-pointer hover:scale-105 transition-transform duration-300"
                onClick={() => setIsOpen(true)}
            >
                <div className="h-64 bg-gray-800 flex items-center justify-center overflow-hidden">
                    {hasPoster ? (
                        <img src={poster} alt={`${title} poster`} className="w-full h-full object-cover" />
                    ) : (
                        <div className="text-gray-400 text-center px-4">
                            <svg width="80" height="80" viewBox="0 0 24 24" fill="none" className="mx-auto mb-2">
                                <rect x="2" y="4" width="20" height="14" rx="2" stroke="currentColor" strokeWidth="1.5" />
                                <path d="M8 12l2.5 3 3.5-4.5L18 16" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
                            </svg>
                            <div className="text-sm">No poster</div>
                        </div>
                    )}
                </div>

                <div className="p-4 flex-1 flex flex-col">
                    <header className="mb-2">
                        <h3 className="text-lg font-semibold text-white">
                            {title} <span className="text-sm text-gray-400">({year || "—"})</span>
                        </h3>
                        <div className="text-xs text-gray-300 mt-1">{genre || "Genre unknown"}</div>
                    </header>
                    <p className="text-sm text-gray-300 mb-3 line-clamp-3">{plot || "No synopsis available."}</p>
                    <div className="mt-auto flex items-center justify-between gap-3">
                        <div className="flex flex-wrap gap-2">
                            {ott_platforms.length ? (
                                ott_platforms.map((p) => (
                                    <span key={p} className="text-xs px-2 py-1 bg-white/6 rounded-full text-gray-100">{p}</span>
                                ))
                            ) : (
                                <span className="text-xs text-gray-500">No OTT data</span>
                            )}
                        </div>
                        <div className="flex items-center gap-2">
                            {trailer ? (
                                <a
                                    href={trailer}
                                    target="_blank"
                                    rel="noopener noreferrer"
                                    className="px-3 py-2 bg-indigo-600 rounded-md text-sm text-white hover:bg-indigo-700"
                                >
                                    ▶ Trailer
                                </a>
                            ) : (
                                <button className="px-3 py-2 bg-gray-700 rounded-md text-sm text-gray-300" disabled>No Trailer</button>
                            )}
                        </div>
                    </div>
                </div>
            </article>

            {/* Modal Overlay */}
            {isOpen && (
                <div
                    className="fixed inset-0 bg-black/70 z-50 flex items-start justify-center p-4 overflow-auto"
                    onClick={() => setIsOpen(false)}
                >
                    <div
                        className="bg-gray-900 rounded-3xl overflow-auto max-w-4xl w-full max-h-[90vh] shadow-xl transform transition-transform duration-300 scale-100 relative
                                   [&::-webkit-scrollbar]:w-2 [&::-webkit-scrollbar-track]:bg-gray-800 [&::-webkit-scrollbar-thumb]:bg-indigo-600 [&::-webkit-scrollbar-thumb]:rounded-full my-8"
                        onClick={(e) => e.stopPropagation()} // prevent closing when clicking inside modal
                    >
                        {/* Close Button */}
                        <button
                            onClick={() => setIsOpen(false)}
                            className="absolute top-4 right-4 text-white text-2xl hover:text-indigo-500 transition-colors z-10"
                        >
                            &times;
                        </button>

                        <div className="flex flex-col lg:flex-row">
                            {/* Poster */}
                            {hasPoster && (
                                <div className="lg:w-1/2 h-96 lg:h-auto bg-black flex items-center justify-center flex-shrink-0">
                                    <img src={poster} alt={`${title} poster`} className="w-full h-full object-contain" />
                                </div>
                            )}

                            {/* Details */}
                            <div className="lg:w-1/2 p-6 flex flex-col text-white overflow-auto [&::-webkit-scrollbar]:w-1 [&::-webkit-scrollbar-track]:bg-gray-800 [&::-webkit-scrollbar-thumb]:bg-indigo-500 [&::-webkit-scrollbar-thumb]:rounded-full">
                                <h2 className="text-2xl font-bold mb-2">{title} <span className="text-gray-400 text-base">({year || "—"})</span></h2>
                                <p className="text-gray-300 mb-2"><strong>Genre:</strong> {genre || "Unknown"}</p>
                                <p className="text-gray-300 mb-2"><strong>Director:</strong> {director || "N/A"}</p>
                                {imdb_rating && <p className="text-gray-300 mb-2"><strong>IMDb Rating:</strong> {imdb_rating}</p>}
                                <p className="text-gray-300 mb-4"><strong>Plot:</strong> {plot || "No synopsis available."}</p>
                                <div className="mb-4 flex flex-wrap gap-2">
                                    {ott_platforms.length
                                        ? ott_platforms.map((p) => (
                                            <span key={p} className="px-3 py-1 bg-indigo-600 rounded-full text-white text-sm">{p}</span>
                                        ))
                                        : <span className="text-gray-400 text-sm">No OTT info</span>
                                    }
                                </div>
                                {trailer && (
                                    <a
                                        href={trailer}
                                        target="_blank"
                                        rel="noopener noreferrer"
                                        className="px-4 py-2 bg-indigo-500 rounded-lg hover:bg-indigo-600 text-white text-sm w-max"
                                    >
                                        ▶ Watch Trailer
                                    </a>
                                )}
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </>
    );
}
