import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
import requests
import google.generativeai as genai
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv


# Show ASCII art from art file
def show_ascii_art():
    art_path = os.path.join(os.path.dirname(__file__), 'art')
    if os.path.exists(art_path):
        with open(art_path, 'r', encoding='utf-8') as f:
            print(f.read())
    else:
        print("[ascii art missing]")

show_ascii_art()
# Load environment variables from .env
load_dotenv()

# Configure Gemini client with API key from environment
genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))
model_name = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')

# 1. Generate a curiosity with AI
def generate_curiosity():
    model = genai.GenerativeModel(model_name)
    response = model.generate_content("Tell me a short and interesting fun fact that could be used to create a 15-second video in a short sentence that lasts 15 seconds.")
    return response.text.strip()

def generate_image_query():
    def inner(curiosity):
        model = genai.GenerativeModel(model_name)
        prompt = f"Based on this fun fact, give me a one-word image suggestion that could illustrate this fun fact: {curiosity}"
        response = model.generate_content(prompt)
        print(f"✅ Image suggestion: {response.text.strip()}")
        return response.text.strip()
    return inner

# Use the Unsplash API to fetch a relevant image based on the fun fact
def download_image():
    def inner(curiosity):
        # Get Unsplash API key from environment
        unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
        if not unsplash_access_key:
            raise Exception("UNSPLASH_ACCESS_KEY not set in environment variables.")

        # Use the fun fact as a search query
        query = generate_image_query()(curiosity)
        search_url = "https://api.unsplash.com/search/photos"
        params = {
            "query": query,
            "orientation": "portrait",
            "per_page": 1
        }
        headers = {
            "Authorization": f"Client-ID {unsplash_access_key}"
        }
        response = requests.get(search_url, params=params, headers=headers)
        if response.status_code == 200:
            data = response.json()
            if data["results"]:
                image_url = data["results"][0]["urls"]["regular"]
                img_path = "content/image.jpg"
                img_response = requests.get(image_url)
                if img_response.status_code == 200 and img_response.headers.get('Content-Type', '').startswith('image/'):
                    with open(img_path, "wb") as f:
                        f.write(img_response.content)
                    return img_path
                else:
                    raise Exception(f"Failed to download image from Unsplash. Status: {img_response.status_code}, Content-Type: {img_response.headers.get('Content-Type')}")
            else:
                raise Exception("No images found for the given query on Unsplash.")
        else:
            raise Exception(f"Failed to search Unsplash API. Status: {response.status_code}, Response: {response.text}")
    return inner

# 3. Generate audio with gTTS
def generate_audio(text):
    tts = gTTS(text=text, lang='en')
    audio_path = "content/audio.mp3"
    tts.save(audio_path)
    return audio_path

# 3.1 Generate audio with ElevenLabs
def generate_audio_with_elevenlabs(text):
    elevenlabs_api_key = os.environ.get("ELEVEN_LAB_API_KEY")
    if not elevenlabs_api_key:
        raise Exception("ELEVEN_LAB_API_KEY not set in environment variables.")
    # Initialize ElevenLabs client with API key
    elevenlabs = ElevenLabs(
        api_key=elevenlabs_api_key,
    )

    audio_stream = elevenlabs.text_to_speech.convert(
        text=text,
        voice_id="JBFqnCBsd6RMkjVDRZzb",
        model_id="eleven_multilingual_v2",
        output_format="mp3_44100_128",
    )
    audio_path = "content/audio.mp3"
    # Save the audio stream chunk by chunk
    with open(audio_path, "wb") as f:
        for chunk in audio_stream:
            if chunk:
                f.write(chunk)
    return audio_path

def create_video(image_path, audio_path, text):
    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).with_duration(audio.duration).resized(height=1280)
    image = image.with_position("center").with_audio(audio)

    video = CompositeVideoClip([image])
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path

# Generate fun fact once
fun_fact = generate_curiosity()
print(f"Fun Fact: {fun_fact}")

# Generate image query and download image
image = download_image()(fun_fact)
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

video = create_video(image, audio, fun_fact)

print(f"✅ Video generated: {video}")
