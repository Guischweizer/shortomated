import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video(image_path, audio_path, text):
    os.makedirs("content", exist_ok=True)
    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).with_duration(audio.duration).resized(height=1280)
    image = image.with_position("center").with_audio(audio)
    video = CompositeVideoClip([image])
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path
