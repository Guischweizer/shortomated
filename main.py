import os
from gtts import gTTS
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip
import requests
import google.generativeai as genai
from dotenv import load_dotenv

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
    url = "https://source.unsplash.com/random/720x1280"
    img_path = "content/imagem.jpg"
    response = requests.get(url)
    # Check if the response is an image
    if response.status_code == 200 and response.headers.get('Content-Type', '').startswith('image/'):
        with open(img_path, "wb") as f:
            f.write(response.content)
        return img_path
    else:
        raise Exception(f"Failed to download a valid image. Status: {response.status_code}, Content-Type: {response.headers.get('Content-Type')}")

# 3. Generate audio with gTTS
def gerar_audio(texto):
    tts = gTTS(text=texto, lang='pt')
    audio_path = "content/audio.mp3"
    tts.save(audio_path)
    return audio_path

# 4. Build video with image + audio
def create_video(imagem_path, audio_path, texto):
    audio = AudioFileClip(audio_path)
    imagem = ImageClip(imagem_path).set_duration(audio.duration).resize(height=1280)
    imagem = imagem.set_position("center").set_audio(audio)

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
