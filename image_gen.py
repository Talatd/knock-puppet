import requests
import urllib.parse
from pathlib import Path

CHARACTER_BASE = "A weathered, hand-carved wooden marionette puppet of a 1970s Vietnam soldier, wearing a tattered olive-drab uniform, a faded headband, visible wood grain texture, vintage doll joints."
STYLE_BASE = "watercolor and charcoal sketch style, moody cinematic lighting, dark vignetted background, 4k, artistic, no text"
DEFAULT_SEED = 12345

MOOD_VISUALS = {
    "weary":         "hanging loosely from tangled strings, head bowed, exhausted expression",
    "nostalgic":     "looking closely at a small faded photograph in its wooden hands, warm soft lighting",
    "accepting":     "strings being cut and falling, looking upwards towards a soft golden light, peaceful",
    "fading":        "dissolving into glowing dust particles, silhouette against a bright doorway",
    "angry":         "clenched wooden fists, harsh red lighting, aggressive posture, tangled strings",
    "afraid":        "huddled in a dark corner, wide hollow eyes, deep blue shadows, trembling",
    "hallucinating": "surreal perspective, melting surroundings, neon jungle colors, distorted proportions",
    "regretful":     "kneeling in thick mud, rain pouring down, somber grey tones, head in hands"
}

def generate_puppet_image(mood: str, output_dir: str = "/tmp") -> str:
    Path(output_dir).mkdir(parents=True, exist_ok=True)
    
    mood_desc = MOOD_VISUALS.get(mood, MOOD_VISUALS["weary"])
    full_prompt = f"{CHARACTER_BASE}, {mood_desc}, {STYLE_BASE}"
    encoded_prompt = urllib.parse.quote(full_prompt)
    
    image_url = f"https://image.pollinations.ai/prompt/{encoded_prompt}?width=1024&height=1024&nologo=true&seed={DEFAULT_SEED}"
    
    try:
        response = requests.get(image_url)
        if response.status_code == 200:
            filename = f"{output_dir}/puppet_{mood}.png"
            with open(filename, "wb") as f:
                f.write(response.content)
            return filename
        else:
            return ""
    except Exception:
        return ""
