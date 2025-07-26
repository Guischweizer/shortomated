# Shortomated


Shortomated is an automated Python tool that generates short vertical videos based on interesting facts (curiosities) using AI. It fetches a curiosity, generates a relevant image using the Unsplash API, creates an audio narration with gTTS or ElevenLabs, and combines them into a video using MoviePy.

## Features
- Generates a short curiosity using Google Gemini AI
- Searches Unsplash for a relevant image based on the curiosity
- Converts the curiosity text to audio using gTTS (Google Text-to-Speech) or ElevenLabs (high quality, multi-language TTS)
- Creates a vertical video (720x1280) with image and audio
- Displays ASCII art on startup

## Requirements
- Python 3.8+
- See `requirements.txt` for all dependencies

## Setup
1. Clone the repository:
   ```bash
   git clone https://github.com/Guischweizer/shortomated.git
   cd shortomated
   ```
2. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in the project root with the following variables:
   ```env
   GEMINI_API_KEY=your_gemini_api_key
   UNSPLASH_ACCESS_KEY=your_unsplash_access_key
   # For ElevenLabs TTS support (optional, but recommended for high quality voices):
   ELEVEN_LAB_API_KEY=your_elevenlabs_api_key
   # Optionally override the Gemini model:
   # GEMINI_MODEL=gemini-1.5-flash
   ```

## Usage

Run the main script:
```bash
python main.py
```

By default, the script will use ElevenLabs for audio if the API key is set, otherwise it will fall back to gTTS. The script prints ASCII art, generates a fun fact, fetches a relevant image, creates audio, and produces a video in the `content/` directory.

## Notes
- The Unsplash API is used for image search. You need to register for a free API key at [Unsplash Developers](https://unsplash.com/developers).
- The Gemini API key is required for AI text generation.
- The ElevenLabs API key is required for high quality TTS (see https://elevenlabs.io/ for a free API key).
- The output video and assets are saved in the `content/` directory.

## License
MIT License
