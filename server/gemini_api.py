import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()
GEN_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEN_API_KEY)

def get_suggested_genres(user_input: str):
    try:
        prompt = f"""Based on this user input: "{user_input}"
Suggest exactly 3-5 popular movie genres that best match their mood or preferences.
Return ONLY the genres as a comma-separated list, no extra text.
Examples: Action, Comedy, Drama, Romance, Thriller, Horror, Adventure, Fantasy, Sci-Fi, Animation, Family, Crime, Mystery, War, Biography
"""
        model = genai.GenerativeModel("gemini-2.0-flash-exp")
        response = model.generate_content(prompt)
        text = response.text.strip()
        suggestions = [g.strip("- ").strip() for g in text.split(",") if g.strip()]
        return suggestions[:5]

    except Exception as e:
        print(f"Error interacting with Gemini API: {e}")
        return ["Adventure", "Comedy", "Action"]
