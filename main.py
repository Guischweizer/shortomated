import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
import requests
import google.generativeai as genai
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
    response = model.generate_content("Me diga uma curiosidade curta e interessante")
    return response.text.strip()

#TODO Update this function to fetch a good image (currently it uses a random image from Unsplash)
#TODO Use the unsplash API to fetch a relevant image based on the curiosity and make the proper authentication
def download_image():
    # Get Unsplash API key from environment
    unsplash_access_key = os.environ.get("UNSPLASH_ACCESS_KEY")
    if not unsplash_access_key:
        raise Exception("UNSPLASH_ACCESS_KEY not set in environment variables.")

    # Use the curiosity text as a search query
    query = generate_curiosity()
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
            img_path = "content/imagem.jpg"
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

# 3. Generate audio with gTTS
def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt')
    audio_path = "content/audio.mp3"
    tts.save(audio_path)
    return audio_path

# 4. Build video with image + audio
def create_video(imagem_path, audio_path, texto):
    audio = AudioFileClip(audio_path)
    imagem = ImageClip(imagem_path).with_duration(audio.duration).resized(height=1280)
    imagem = imagem.with_position("center").with_audio(audio)

    video = CompositeVideoClip([imagem])
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path

# Execute the steps to create the video
texto = generate_curiosity()
print(f"Curiosidade: {texto}")

imagem = download_image()
audio = gerar_audio(texto)
video = create_video(imagem, audio, texto)

print(f"✅ Vídeo gerado: {video}")
