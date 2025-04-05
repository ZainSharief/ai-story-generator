from google.cloud import texttospeech_v1beta1 as texttospeech
import os

def text_to_speech(text: str, out_file: str) -> None:
    '''
    Converts text to speech and saves it as an MP3 file, also printing timepoints.

    text: str: The text to convert to speech.
    out_file: str: The path to save the MP3 file.
    '''

    assert os.path.exists("credentials.json"), "Error: credentials.json not found."

    # Set the environment variable
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "credentials.json"

    # Prepare SSML with properly formatted marks
    words = text.split()
    ssml_text = "<speak>"
    for i, word in enumerate(words):
        ssml_text += f'<mark name="word_{i}"/>{word} '
    ssml_text += "</speak>"

    # Create a client instance
    client = texttospeech.TextToSpeechClient()

    # Use ssml_input instead of text input
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml_text)
    
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", name="en-US-Neural2-J"
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )

    # Create the request with time pointing correctly specified
    request = texttospeech.SynthesizeSpeechRequest(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
        enable_time_pointing=[texttospeech.SynthesizeSpeechRequest.TimepointType.SSML_MARK]
    )
    
    # Call synthesize_speech with the request object
    response = client.synthesize_speech(request)

    with open(out_file, "wb") as out:
        out.write(response.audio_content)

    return response.timepoints

if __name__ == '__main__':
    text = "This is a test."
    out_file = "test.mp3"

    text_to_speech(text, out_file)