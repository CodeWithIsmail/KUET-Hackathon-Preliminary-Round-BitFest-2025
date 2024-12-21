# import os
# import google.generativeai as genai

# # Configure the API key
# genai.configure(api_key='AIzaSyBm8CyN3tCYHp2QsvSTA-2FeNNppB_Wyms')

# # Initialize the Gemini 1.5 Flash model
# model = genai.GenerativeModel("gemini-1.5-flash")

# # Define your hardcoded prompt
# prompt = "Write a short story about a cat who goes on an adventure."

# # Generate text using the model
# response = model.generate_content(prompt)

# # Print the generated text
# print(response.text)

import os
import google.generativeai as genai
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Configure the Gemini API key
genai.configure(api_key='AIzaSyBm8CyN3tCYHp2QsvSTA-2FeNNppB_Wyms')

# Initialize the Gemini 1.5 Flash model
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/generate_text', methods=['POST'])
def generate_text():
    try:
        # Get the prompt from the JSON request body
        data = request.get_json()
        prompt = data.get("prompt", None)

        if not prompt:
            return jsonify({"error": "Prompt is required"}), 400

        # Generate text using the Gemini model
        response = model.generate_content(prompt)
        
        # Return the generated text as a response
        return jsonify({"generated_text": response.text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

