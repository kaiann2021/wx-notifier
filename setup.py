import os
import json

CONFIG_FILE = 'config.json'

def setup_config():
    print("--- Configuration Setup ---")
    print("Please provide the necessary credentials.")
    
    # 1. Request Token
    token = input("Enter the Request Token (for /notify API): ").strip()
    if not token:
        print("Token cannot be empty.")
        return

    # 2. WeCom Credentials
    corpid = input("Enter WeCom CorpID (企业ID): ").strip()
    agentid = input("Enter WeCom AgentID (应用ID): ").strip()
    corpsecret = input("Enter WeCom Secret (应用Secret): ").strip()

    config = {
        "auth_token": token,
        "corpid": corpid,
        "agentid": agentid,
        "corpsecret": corpsecret
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"Configuration saved to {CONFIG_FILE}")

def main():
    setup_config()
    print("\nSetup complete! You can now run 'python app.py'")

if __name__ == "__main__":
    main()
