export default function Loader({ text = "Hold on, analyzing your vibe..." }) {
    return (
        <div className="flex flex-col items-center justify-center py-8">
            <div
                className="w-12 h-12 border-4 border-t-transparent rounded-full animate-spin"
                role="status"
                aria-label="loading"
                style={{ borderColor: "rgba(255,255,255,0.2)" }}
            />
            <p className="mt-3 text-sm text-gray-300 text-center">{text}</p>
        </div>
    );
}
