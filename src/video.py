import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
import re

def create_video(image_path, audio_path, text):
    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).with_duration(audio.duration).resized(height=1280)
    image = image.with_position("center").with_audio(audio)

    # Use a reliable system font for the text overlay
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    if not os.path.exists(font_path):
        font_path = None  # fallback to default if not found


    # --- Subtitle logic ---
    # Split text into sentences
    sentences = re.split(r'(?<=[.!?]) +', text)
    n = len(sentences)
    duration_per_sentence = audio.duration / n if n > 0 else audio.duration

    subtitle_clips = []
    for i, sentence in enumerate(sentences):
        start = i * duration_per_sentence
        end = start + duration_per_sentence
        subtitle = TextClip(
            text=sentence,
            font=font_path,
            font_size=20,
            color='black'
        ).with_position('center').with_start(start).with_duration(duration_per_sentence)
        subtitle_clips.append(subtitle)

    video = CompositeVideoClip([image] + subtitle_clips)
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path
