from flask import Flask, request, jsonify
import json
import os
from cryptography.fernet import Fernet
from client import WeComClient

app = Flask(__name__)

# Configuration Paths
DATA_DIR = 'data'
CONFIG_FILE = 'config.json'
KEY_FILE = os.path.join(DATA_DIR, 'secret.key')
TOKEN_FILE = os.path.join(DATA_DIR, 'token.bin')

# Global variables
client = None
valid_token = None

def load_config_and_token():
    global client, valid_token
    
    # 1. Load WeCom Config
    if not os.path.exists(CONFIG_FILE):
        print(f"Error: {CONFIG_FILE} not found. Please run setup.py first.")
        return False

    with open(CONFIG_FILE, 'r') as f:
        config = json.load(f)
        client = WeComClient(
            corpid=config.get('corpid'),
            corpsecret=config.get('corpsecret'),
            agentid=config.get('agentid')
        )

    # 2. Load and Decrypt Request Token
    if not os.path.exists(KEY_FILE) or not os.path.exists(TOKEN_FILE):
        print("Error: security tokens not found. Please run setup.py first.")
        return False

    try:
        with open(KEY_FILE, 'rb') as f:
            key = f.read()
        
        cipher_suite = Fernet(key)
        
        with open(TOKEN_FILE, 'rb') as f:
            encrypted_token = f.read()
            
        valid_token = cipher_suite.decrypt(encrypted_token).decode()
        print("Configuration and tokens loaded successfully.")
        return True
    
    except Exception as e:
        print(f"Error loading secrets: {e}")
        return False

@app.route('/notify', methods=['GET'])
def notify():
    # Helper to check init
    if not client or not valid_token:
        # Try loading again if potentially not initialized (though main does it)
        if not load_config_and_token():
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
    if load_config_and_token():
        # Listen on all interfaces, port 8080 or configurable
        port = 8080
        print(f"Starting server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port)
    else:
        print("Failed to start application due to configuration errors.")
