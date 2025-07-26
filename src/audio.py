import os
from gtts import gTTS
from elevenlabs.client import ElevenLabs

def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_path = "content/audio.mp3"
    tts.save(audio_path)
    return audio_path

def generate_audio_with_elevenlabs(text):
    elevenlabs_api_key = os.environ.get("ELEVEN_LAB_API_KEY")
    if not elevenlabs_api_key:
        raise Exception("ELEVEN_LAB_API_KEY not set in environment variables.")
    elevenlabs = ElevenLabs(api_key=elevenlabs_api_key)
    audio_stream = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_path = "content/audio.mp3"
    with open(audio_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    return audio_path
