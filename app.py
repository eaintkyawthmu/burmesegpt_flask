import json
import os
import requests
from flask import Flask, jsonify, request, send_from_directory

# Load model directly
from transformers import AutoTokenizer, AutoModelForCausalLM

tokenizer = AutoTokenizer.from_pretrained("WYNN747/Burmese-GPT-main-sentence")
model = AutoModelForCausalLM.from_pretrained("WYNN747/Burmese-GPT-main-sentence")

def query(payload, max_length=200, min_length=10, num_return_sequences=3):
    data = {
        "inputs": payload,
        "parameters": {
            "max_length": max_length,  # <-- Adjusted to control maximum length
            "min_length": min_length,
            "num_return_sequences": num_return_sequences
        }
    }

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

            # Tokenize the prompt
            input_ids = tokenizer.encode(prompt, return_tensors="pt")

            # Generate text using the model
            generated_ids = model.generate(input_ids, max_length=500)  # Adjust max_length as needed
            generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)

            # Return the generated text as a JSON response
            return jsonify({"generated_text": generated_text})
        else:
            return jsonify({"error": "No prompt provided"})


@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('web', path)

if __name__ == "__main__":
    app.run(debug=True)
