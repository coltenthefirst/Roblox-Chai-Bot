import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/chai_api', methods=['POST'])
def chat():
    print("Received request for /chai_api")
    try:
        api_key = request.headers.get('KEY')
        print(f"API Key from header: {api_key}")
        if not api_key:
            print("No API key found in headers.")
            return jsonify({"error": "API key missing"}), 400
        
        content = request.json.get('content')
        print(f"Content from JSON body: {content}")
        if not content:
            print("No content found in JSON payload.")
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

        print("Sending request to Chai API...")
        response = requests.post(url, json=payload, headers=headers)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        
        return jsonify(response.json())
    
    except Exception as e:
        print("Error during /chai_api handling:", str(e))
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    print("Starting Flask app on port", port, "with debug =", debug_mode)
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
