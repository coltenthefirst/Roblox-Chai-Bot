import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chai_api', methods=['POST'])
def chat():
    api_key = request.headers.get('X-API_KEY')
    if not api_key:
        return jsonify({"error": "API key missing"}), 400
    content = request.json.get('content')
    if not content:
        return jsonify({"error": "Content missing"}), 400
    url = "https://api.chai-research.com/v1/chat/completions"
    payload = {
        "model": "chai_v1",
        "messages": [
            {
                "role": "ai",
                "content": content
            }
        ]
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-API_KEY": api_key
    }
    response = requests.post(url, json=payload, headers=headers)
    return jsonify(response.json())

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
