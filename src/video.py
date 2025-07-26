import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip

def create_video(image_path, audio_path, text):
    audio = AudioFileClip(audio_path)
    image = ImageClip(image_path).with_duration(audio.duration).resized(height=1280)
    image = image.with_position("center").with_audio(audio)

    # Use a reliable system font for the text overlay
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    if not os.path.exists(font_path):
        font_path = None  # fallback to default if not found

    txt_clip = TextClip(
        text=text,
        font=font_path,
        font_size=20,
        color='black'
    ).with_position('center').with_duration(audio.duration)

    video = CompositeVideoClip([image, txt_clip])
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path
