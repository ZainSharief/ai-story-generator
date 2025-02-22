from google.cloud import texttospeech
import os

def text_to_speech(text: str, out_file: str) -> None:

    '''
    Converts text to speech and saves it as an MP3 file.

    text: str: The text to convert to speech.
    out_file: str: The path to save the MP3 file.
    '''

    # Set the environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

    # Create a client instance
    client = texttospeech.TextToSpeechClient()

    # Changes the settings of the text to speech
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Neural2-J"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Synthesizes the text to speech
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )

    with open(out_file, "wb") as out:
        out.write(response.audio_content)

if __name__ == '__main__':

    text = "This is a test."
    out_file = "test.mp3"

    text_to_speech(text, out_file)