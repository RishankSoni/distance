from flask import Flask, request, jsonify
import subprocess
import pyttsx3
import os

app = Flask(__name__)

@app.route('/speak', methods=['POST'])
def speak():
    # 1. Get the text from the JSON request
    data = request.get_json()

    # Default to "Hello World" if no text is provided
    text_to_speak = data.get('text', 'Hello World')

    filename = 'test.wav'

    try:
        # --- Your TTS Logic ---
        # Initialize the engine
        engine = pyttsx3.init()

        # Save the dynamic text to file instead of static 'Hello World'
        engine.save_to_file(text_to_speak, filename)
        engine.runAndWait()

        # --- Your Playback Logic ---
        # Plays the file using the specific hardware device (plughw:2,0)
        # We use check=True to raise an error if aplay fails
        # Change plug accordingly 
        subprocess.run(["aplay", "-D", "plugw:0,0", filename], check=True)

        return jsonify({
            "status": "success",
            "message": f"Successfully played: '{text_to_speak}'"
        }), 200

    except Exception as e:
        return jsonify({
            "status": "error",
            "error": str(e)
        }), 500

if __name__ == '__main__':
    # Runs on all available IPs on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
