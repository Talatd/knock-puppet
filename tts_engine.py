import os
import requests
import json
import base64
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY")

def generate_speech(text, filename="response.mp3"):
    if not API_KEY:
        return None

    url = f"https://texttospeech.googleapis.com/v1/text:synthesize?key={API_KEY}"

    ssml_text = f"""
    <speak>
      <prosody rate="85%" pitch="-2st">
        {text}
      </prosody>
    </speak>
    """

    payload = {
        "input": {"ssml": ssml_text},
        "voice": {
            "languageCode": "en-US",
            "name": "en-US-Neural2-D",
            "ssmlGender": "MALE"
        },
        "audioConfig": {
            "audioEncoding": "MP3",
            "effectsProfileId": ["small-bluetooth-speaker-class-device"]
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        
        data = response.json()
        audio_content = base64.b64decode(data["audioContent"])

        file_path = os.path.join("/tmp", filename)
        with open(file_path, "wb") as out:
            out.write(audio_content)
            
        return filename
    except Exception:
        return None
