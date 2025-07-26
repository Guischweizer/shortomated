import os
from moviepy import ImageClip, AudioFileClip, CompositeVideoClip, TextClip
import re

def create_video(image_paths, audio_path, text):
    """
    image_paths: list of at least 3 image file paths
    audio_path: path to audio file
    text: subtitle text
    """
    audio = AudioFileClip(audio_path)

    # Calculate duration per slide
    num_slides = max(3, len(image_paths))
    slide_duration = audio.duration / num_slides

    # Create slides (ImageClips)
    slides = []
    for i in range(num_slides):
        img_path = image_paths[i % len(image_paths)]  # repeat if less than 3
        img_clip = ImageClip(img_path).with_duration(slide_duration).resized(height=1280)
        img_clip = img_clip.with_position("center")
        slides.append(img_clip)

    # Concatenate slides
    from moviepy import concatenate_videoclips
    video_bg = concatenate_videoclips(slides).with_audio(audio)

    # Use a reliable system font for the text overlay
    font_path = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
    if not os.path.exists(font_path):
        font_path = None  # fallback to default if not found


    # --- Subtitle logic ---
    sentences = re.split(r'(?<=[.!?]) +', text)
    n = len(sentences)
    duration_per_sentence = audio.duration / n if n > 0 else audio.duration

    subtitle_clips = []
    for i, sentence in enumerate(sentences):
        start = i * duration_per_sentence
        subtitle = TextClip(
            text=sentence,
            font=font_path,
            font_size=30,
            color='black',
            method='caption',
            size=(video_bg.w - 80, None)  # leave some margin on sides
        ).with_position(('center')).with_start(start).with_duration(duration_per_sentence)
        subtitle_clips.append(subtitle)

    video = CompositeVideoClip([video_bg] + subtitle_clips)
    video_path = "content/short.mp4"
    video.write_videofile(video_path, fps=24)
    return video_path
