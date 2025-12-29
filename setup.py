import os
import json
import getpass
from cryptography.fernet import Fernet

DATA_DIR = 'data'
CONFIG_FILE = 'config.json'
KEY_FILE = os.path.join(DATA_DIR, 'secret.key')
TOKEN_FILE = os.path.join(DATA_DIR, 'token.bin')

def ensure_data_dir():
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

def generate_key_and_token():
    print("--- Security Setup ---")
    print("This token will be used to authenticate requests to your /notify API.")
    # Use input instead of getpass for simplicity in some environments, or just typical input
    token = input("Enter the secret Request Token (e.g. my-secret-pword): ").strip()
    
    if not token:
        print("Token cannot be empty.")
        return

    # Generate key
    key = Fernet.generate_key()
    cipher_suite = Fernet(key)
    encrypted_token = cipher_suite.encrypt(token.encode())

    # Save key
    with open(KEY_FILE, 'wb') as f:
        f.write(key)
    
    # Save encrypted token
    with open(TOKEN_FILE, 'wb') as f:
        f.write(encrypted_token)
    
    print(f"Key saved to {KEY_FILE}")
    print(f"Token encrypted and saved to {TOKEN_FILE}")

def setup_wecom_config():
    print("\n--- WeCom App Configuration ---")
    corpid = input("Enter WeCom CorpID (企业ID): ").strip()
    agentid = input("Enter WeCom AgentID (应用ID): ").strip()
    corpsecret = input("Enter WeCom Secret (应用Secret): ").strip()

    config = {
        "corpid": corpid,
        "agentid": agentid,
        "corpsecret": corpsecret
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Configuration saved to {CONFIG_FILE}")

def main():
    ensure_data_dir()
    generate_key_and_token()
    setup_wecom_config()
    print("\nSetup complete! You can now run 'python app.py'")

if __name__ == "__main__":
    main()
