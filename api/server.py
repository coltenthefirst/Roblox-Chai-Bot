import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/api/chat', methods=['POST'])
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
    app.run(debug=True)