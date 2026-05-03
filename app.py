from flask import Flask, render_template, request, jsonify, send_from_directory
from llm_agent import get_puppet_response, detect_mood
from image_gen import generate_puppet_image
from tts_engine import generate_speech
import os
import time

app = Flask(__name__)
conversation_history = []
current_puppet_mood = "weary"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tmp/<path:filename>")
def serve_tmp(filename):
    return send_from_directory("/tmp", filename)

@app.route("/chat", methods=["POST"])
def chat():
    global conversation_history, current_puppet_mood
    
    user_message = request.json.get("message", "")
    prev_mood = current_puppet_mood
    current_puppet_mood = detect_mood(user_message, current_puppet_mood)
    
    puppet_response = get_puppet_response(user_message, conversation_history, current_puppet_mood)
    
    conversation_history.append({"role": "user", "content": user_message})
    conversation_history.append({"role": "assistant", "content": puppet_response})
    
    image_path = None
    if current_puppet_mood != prev_mood:
        image_path = generate_puppet_image(current_puppet_mood)
        if image_path:
            image_path = image_path.replace("/tmp/", "")
    
    audio_file = f"speech_{int(time.time())}.mp3"
    audio_path = generate_speech(puppet_response, audio_file)
    
    return jsonify({
        "response": puppet_response,
        "mood": current_puppet_mood,
        "image": image_path,
        "audio": audio_path
    })

@app.route("/reset", methods=["POST"])
def reset():
    global conversation_history, current_puppet_mood
    conversation_history = []
    current_puppet_mood = "weary"
    
    image_path = generate_puppet_image("weary")
    if image_path:
        image_path = image_path.replace("/tmp/", "")
        
    return jsonify({"status": "reset", "image": image_path})

if __name__ == "__main__":
    app.run(debug=True)
