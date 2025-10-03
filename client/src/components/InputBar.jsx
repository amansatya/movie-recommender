import { useState } from "react";

/**
 * Props:
 *  - onSubmit: function(mood: string) => void
 *  - placeholder?: string
 *  - disabled?: boolean
 */
export default function InputBar({ onSubmit, placeholder = "Enter mood or genre...", disabled = false }) {
    const [value, setValue] = useState("");

    const submit = (e) => {
        if (e) e.preventDefault();
        const trimmed = value.trim();
        if (!trimmed || !onSubmit) return;
        onSubmit(trimmed);
        setValue(""); // clear input after submit
    };

    return (
        <form onSubmit={submit} className="w-full flex gap-3 items-center">
            <label htmlFor="mood-input" className="sr-only">Mood or Genre</label>
            <input
                id="mood-input"
                type="text"
                value={value}
                onChange={(e) => setValue(e.target.value)}
                placeholder={placeholder}
                disabled={disabled}
                onKeyDown={(e) => { if (e.key === "Enter") submit(e); }}
                className="flex-1 px-4 py-3 rounded-lg bg-white/5 placeholder-gray-400 text-white focus:outline-none focus:ring-2 focus:ring-indigo-500"
                aria-label="Enter mood or genre"
            />
            <button
                type="submit"
                disabled={disabled}
                className="cursor-pointer px-4 py-3 bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 rounded-lg text-white font-medium"
                aria-disabled={disabled}
            >
                Search
            </button>
        </form>
    );
}
