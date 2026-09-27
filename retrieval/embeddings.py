import os
import time
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

def get_embedding(text: str, retries: int = 3, delay: int = 5) -> list[float]:
    """
    Converts text into an embedding vector, with retry logic to handle
    temporary server errors during batch embedding of many chunks.
    """
    for attempt in range(retries):
        try:
            result = client.models.embed_content(
                model="gemini-embedding-001",
                contents=text
            )
            return result.embeddings[0].values
        except Exception as e:
            print(f"Embedding attempt {attempt + 1} failed: {e}")
            if attempt < retries - 1:
                time.sleep(delay)

    raise RuntimeError("Failed to generate embedding after multiple attempts.")