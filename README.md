# Shortomated

Shortomated is an automated Python tool that generates short vertical videos based on interesting facts (curiosities) using AI. It fetches a curiosity, generates a relevant image using the Unsplash API, creates an audio narration with gTTS, and combines them into a video using MoviePy.

## Features
- Generates a short curiosity using Google Gemini AI
- Searches Unsplash for a relevant image based on the curiosity
- Converts the curiosity text to audio (Portuguese) using gTTS
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
   # Optionally override the Gemini model:
   # GEMINI_MODEL=gemini-1.5-flash
   ```

## Usage
Run the main script:
```bash
python main.py
```
- The script will print an ASCII art, generate a curiosity, fetch a relevant image, create audio, and produce a video in the `content/` directory.

## Notes
- The Unsplash API is used for image search. You need to register for a free API key at [Unsplash Developers](https://unsplash.com/developers).
- The Gemini API key is required for AI text generation.
- The output video and assets are saved in the `content/` directory.

## License
MIT License
