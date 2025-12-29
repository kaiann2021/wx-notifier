from flask import Flask, request, jsonify
import json
import os
from client import WeComClient

app = Flask(__name__)

# Configuration Paths
CONFIG_FILE = 'config.json'

# Global variables
client = None
valid_token = None

def load_config():
    global client, valid_token
    
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found. Please run setup.py first.")
        return False

    try:
        with open(CONFIG_FILE, 'r') as f:
            config = json.load(f)
            
            # Load WeCom Client
            client = WeComClient(
                corpid=config.get('corpid'),
                corpsecret=config.get('corpsecret'),
                agentid=config.get('agentid')
            )
            
            # Load Auth Token
            valid_token = config.get('auth_token')
            
            if not valid_token:
                print("Error: 'auth_token' is missing in config.json")
                return False
                
        print("Configuration loaded successfully.")
        return True
    
    except Exception as e:
        print(f"Error loading config: {e}")
        return False

@app.route('/notify', methods=['GET'])
def notify():
    # Helper to check init
    if not client or not valid_token:
        if not load_config():
            return jsonify({"error": "Server not configured properly"}), 500

    # 1. Auth Check
    req_token = request.args.get('token')
    if req_token != valid_token:
        return jsonify({"error": "Unauthorized: Invalid token"}), 401

    # 2. Get Params
    title = request.args.get('title', 'Notification')
    body = request.args.get('body', '')

    if not body:
         return jsonify({"error": "Missing 'body' parameter"}), 400

    # 3. Send Message
    result = client.send_text(title, body)
    
    if result.get('errcode') == 0:
        return jsonify({"status": "success", "wecom_response": result}), 200
    else:
        return jsonify({"status": "failed", "wecom_response": result}), 500

if __name__ == '__main__':
    if load_config():
        port = 8080
        print(f"Starting server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port)
    else:
        print("Failed to start application due to configuration errors.")
