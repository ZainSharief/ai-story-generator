from google import genai
from dotenv import load_dotenv
import os

def story_generator(prompt: str) -> str:

    '''
    Generates a story based on the given prompt.
    
    prompt: The prompt given to the AI to generate the story.
    '''

    # Loads the API key from the .env file
    load_dotenv()
    API_KEY = os.getenv("API_KEY")

    client = genai.Client(api_key=API_KEY)
    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt,
    )

    return response.text