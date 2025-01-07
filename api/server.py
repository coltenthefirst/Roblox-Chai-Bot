import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

user_conversations = {}

@app.route('/chai_api', methods=['POST'])
def chat():
    print("Received request for /chai_api")
    try:
        api_key = request.headers.get('KEY')
        print(f"API Key from header: {api_key}")
        
        if not api_key:
            print("No API key found in headers.")
            return jsonify({"error": "API key missing"}), 400
        
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({"error": "User ID missing"}), 400

        conversation_history = user_conversations.get(user_id, [])
        
        content = request.json.get('content')
        print(f"Content from JSON body: {content}")
        
        if not content:
            print("No content found in JSON payload.")
            return jsonify({"error": "Content missing"}), 400

        conversation_history.append({"role": "Me", "message": content})

        payload = {
            "model": "chai_v1",
            "messages": [{"role": entry['role'], "content": entry['message']} for entry in conversation_history]
        }
        
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API_KEY": api_key
        }

        print("Sending request to Chai API...")
        response = requests.post("https://api.chai-research.com/v1/chat/completions", json=payload, headers=headers)
        print("Response status code:", response.status_code)
        print("Response text:", response.text)
        
        if response.status_code == 200:
            bot_response = response.json().get("choices", [{}])[0].get("message", {}).get("content", "No response generated.")
            
            conversation_history.append({"role": "You", "message": bot_response})
            
            user_conversations[user_id] = conversation_history
            
            return jsonify({"bot_response": bot_response})
        else:
            return jsonify({"error": "Chai API returned an error"}), 500

    except Exception as e:
        print("Error during /chai_api handling:", str(e))
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    debug_mode = os.environ.get("FLASK_DEBUG", "False").lower() in ["true", "1"]
    print("Starting Flask app on port", port, "with debug =", debug_mode)
    
    app.run(debug=debug_mode, host='0.0.0.0', port=port)
