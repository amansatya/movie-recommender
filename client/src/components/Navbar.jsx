export default function Navbar() {
    return (
        <header className="w-full bg-gradient-to-r from-indigo-700 to-indigo-900 text-white shadow-sm">
            <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
                <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-lg bg-white/10 flex items-center justify-center font-bold text-lg">MR</div>
                    <h1 className="text-lg font-semibold">Movie Recommender</h1>
                </div>
                <div className="text-sm text-indigo-100/90">React · Tailwind · FastAPI</div>
            </div>
        </header>
    );
}
