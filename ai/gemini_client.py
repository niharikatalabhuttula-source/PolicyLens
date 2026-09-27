import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

MODELS_TO_TRY = ["gemini-3.5-flash", "gemini-3.5-flash-lite"]

def generate_with_retry(prompt: str, retries: int = 3, delay: int = 8) -> str:
    """
    Shared Gemini call with retry + fallback model logic,
    reused across the QA pipeline, summarizer, and info extractor.
    """
    for model_name in MODELS_TO_TRY:
        for attempt in range(retries):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt
                )
                return response.text
            except Exception as e:
                print(f"{model_name} attempt {attempt + 1} failed: {e}")
                if attempt < retries - 1:
                    time.sleep(delay)
        print(f"Giving up on {model_name}, trying next model if available...")

    return "The AI service is currently unavailable. Please try again in a few minutes."