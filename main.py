import sys
from dotenv import load_dotenv
from src.ascii_art import show_ascii_art
from src.curiosity import generate_curiosity
from src.image import download_image
from src.audio import generate_audio, generate_audio_with_elevenlabs
from src.video import create_video
import google.generativeai as genai
import os

load_dotenv()
show_ascii_art()

# Configure Gemini client with API key from environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

# Generate fun fact once
fun_fact = generate_curiosity(model_name)
print(f"Fun Fact: {fun_fact}")

# Generate image query and download image
image = download_image(model_name, fun_fact)
print(f"✅ Image downloaded: {image}")

# Generate audio with ElevenLabs if key is present, otherwise fallback to gTTS
elevenlabs_api_key = os.environ.get("ELEVEN_LAB_API_KEY")
if elevenlabs_api_key:
    audio = generate_audio_with_elevenlabs(fun_fact)
    print(f"✅ Audio generated with ElevenLabs: {audio}")
else:
    print("[INFO] ELEVEN_LAB_API_KEY not found, using gTTS for audio.")
    audio = generate_audio(fun_fact)
    print(f"✅ Audio generated with gTTS: {audio}")

# Create video with the downloaded image and generated audio
video = create_video(image, audio, fun_fact)
print(f"✅ Video generated: {video}")
