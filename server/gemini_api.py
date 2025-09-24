import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
os.environ["GEMINI_API_KEY"] = GEMINI_API_KEY

client = genai.Client()

def get_suggested_genres(user_input: str):
    try:
        prompt = f"""Based on this user input: "{user_input}"

        Suggest exactly 3–5 movie genres that best match their mood or preferences.
        Return only the genres as a comma-separated list with no extra text.

        Examples:
        - Action, Thriller, Adventure
        - Romance, Comedy, Drama
        - Horror, Mystery, Suspense

        User input: {user_input}
        Genres:"""

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        suggestions_text = response.text.strip()
        suggestions = [s.strip("- ").strip() for s in suggestions_text.split(",") if s.strip()]
        return suggestions[:5]

    except Exception as e:
        print(f"Error interacting with Gemini API: {e}")
        return []
