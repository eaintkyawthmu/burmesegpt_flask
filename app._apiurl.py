import json
import os
import requests
from flask import Flask, jsonify, request, send_from_directory

API_URL = "https://api-inference.huggingface.co/models/WYNN747/Burmese-GPT-main-sentence"
headers = {"Authorization": "Bearer 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"}

def query(payload, max_length=200, min_length=10, num_return_sequences=3):
    data = {
        "inputs": payload,
        "parameters": {
            "max_length": max_length,  # <-- Adjusted to control maximum length
            "min_length": min_length,
            "num_return_sequences": num_return_sequences
        }
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

app = Flask(__name__)

@app.route("/")
def index():
    return send_from_directory('web', 'index.html')

@app.route("/api/generate", methods=["POST"])
def generate_api():
    if request.method == "POST":
        prompt = request.json.get('prompt')
        if prompt:
            if not isinstance(prompt, str):
                prompt = str(prompt)  # Ensure prompt is a string

            # Set the desired maximum length here
            desired_length = 00  # Example: Generate up to 500 tokens

            response = query(payload={"inputs": prompt}, max_length=desired_length)
            generated_text = response[0]["generated_text"]
            formatted_response = json.dumps({"generated_text": generated_text})
            return formatted_response
        else:
            return jsonify({"error": "No prompt provided"})

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug=True)
