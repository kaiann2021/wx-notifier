from flask import Flask, request, jsonify, abort
import json
import os
from client import WeComClient
from wechatpy.enterprise.crypto import WeChatCrypto
from wechatpy.exceptions import InvalidSignatureException

app = Flask(__name__)

# Configuration Paths
CONFIG_FILE = 'config.json'

# Global variables
client = None
valid_token = None
wechat_crypto = None
config = {}

def load_config():
    global client, valid_token, wechat_crypto, config
    
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
            
            # Load Crypto for Callback
            callback_token = config.get('callback_token')
            encoding_aes_key = config.get('encoding_aes_key')
            corpid = config.get('corpid')
            
            if callback_token and encoding_aes_key and corpid:
                try:
                    wechat_crypto = WeChatCrypto(callback_token, encoding_aes_key, corpid)
                except Exception as e:
                    print(f"Warning: Failed to initialize WeChatCrypto: {e}")
            
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
    if not client or not valid_token:
        if not load_config():
            return jsonify({"error": "Server not configured properly"}), 500

    req_token = request.args.get('token')
    if req_token != valid_token:
        return jsonify({"error": "Unauthorized: Invalid token"}), 401

    title = request.args.get('title', 'Notification')
    body = request.args.get('body', '')
    touser = request.args.get('touser', '@all')

    if not body:
         return jsonify({"error": "Missing 'body' parameter"}), 400

    result = client.send_text(title, body, touser)
    
    if result.get('errcode') == 0:
        return jsonify({"status": "success", "wecom_response": result}), 200
    else:
        return jsonify({"status": "failed", "wecom_response": result}), 500

@app.route('/callback', methods=['GET', 'POST'])
def callback():
    """
    WeCom Callback URL Verification and Message Handling
    """
    if not wechat_crypto:
        if not load_config() or not wechat_crypto:
            return "Server not configured for callbacks", 500

    msg_signature = request.args.get('msg_signature', '')
    timestamp = request.args.get('timestamp', '')
    nonce = request.args.get('nonce', '')
    echostr = request.args.get('echostr', '')

    if request.method == 'GET':
        # URL Verification
        try:
            decrypted_echo = wechat_crypto.check_signature(
                msg_signature,
                timestamp,
                nonce,
                echostr
            )
            return decrypted_echo
        except InvalidSignatureException:
            abort(403)
        except Exception as e:
            print(f"Validation Error: {e}")
            return "Error", 500
            
    # For POST requests (receiving messages), we just return 'success' logic for now
    # The requirement focused on passing validation.
    return "success"

if __name__ == '__main__':
    if load_config():
        port = 8080
        print(f"Starting server on 0.0.0.0:{port}")
        app.run(host='0.0.0.0', port=port)
    else:
        print("Failed to start application due to configuration errors.")
