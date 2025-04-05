import google.generativeai as genai
from dotenv import load_dotenv
import os

def story_generator(prompt: str) -> str:
    """
    Generates a story based on the given prompt.
    
    prompt: The prompt given to the AI to generate the story.
    """

    # Load API key from .env file
    load_dotenv()
    API_KEY = os.getenv("API_KEY")
    assert API_KEY is not None, "Error: API_KEY not found in the .env file."

    genai.configure(api_key=API_KEY)

    model = genai.GenerativeModel("gemini-2.0-flash") 
    response = model.generate_content(prompt)

    return response.text