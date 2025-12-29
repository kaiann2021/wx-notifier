import os
import json

CONFIG_FILE = 'config.json'

def setup_config():
    print("--- Configuration Setup ---")
    
    # 1. Request Token
    print("\n[Tool Authentication]")
    token = input("Enter the Request Token (for /notify API): ").strip()
    if not token:
        print("Token cannot be empty.")
        return

    # 2. WeCom Credentials
    print("\n[WeCom App Settings]")
    corpid = input("Enter WeCom CorpID (企业ID): ").strip()
    agentid = input("Enter WeCom AgentID (应用ID): ").strip()
    corpsecret = input("Enter WeCom Secret (应用Secret): ").strip()
    
    # 3. WeCom Callback Settings
    print("\n[WeCom Callback Settings]")
    print("These are found in the 'API Reception' (接收消息) section of your app settings.")
    callback_token = input("Enter Callback Token (Token): ").strip()
    encoding_aes_key = input("Enter EncodingAESKey: ").strip()

    config = {
        "auth_token": token,
        "corpid": corpid,
        "agentid": agentid,
        "corpsecret": corpsecret,
        "callback_token": callback_token,
        "encoding_aes_key": encoding_aes_key
    }

    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f, indent=4)
    
    print(f"\nConfiguration saved to {CONFIG_FILE}")

def main():
    setup_config()
    print("\nSetup complete! You can now run 'python app.py'")

if __name__ == "__main__":
    main()
