# WeCom Notifier

A simple HTTP Service to send notifications via Enterprise WeChat (WeCom/WorkWeChat).

## Features
- **Simple API**: Send messages via a GET request.
- **Security**: Token-based authentication.
- **WeCom Callback**: verify callback URL validation for "Receive Messages" execution.
- **Targeted Sending**: Support sending to specific users (`touser`).

## Installation

### Method 1: Python Direct
1.  Clone the repository.
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configuration:
    - Copy `config_example.json` to `config.json`.
    - Fill in your WeCom `corpid`, `agentid`, `corpsecret`, and define your own `auth_token`.
    - (Optional) Fill in `callback_token` and `encoding_aes_key` if you need WeCom validation.
4.  Run:
    ```bash
    python app.py
    ```

### Method 2: Docker
1.  Build image:
    ```bash
    docker build -t wx-notifier .
    ```
2.  Run container (Example mapping config):
    ```bash
    # Prepare your config.json on host first
    docker run -d -p 8080:8080 -v $(pwd)/config.json:/app/config.json wx-notifier
    ```

### Method 3: Docker (Pre-built from GHCR)
1.  Pull the image:
    ```bash
    docker pull ghcr.io/kaiann2021/wx-notifier:main
    ```
2.  Run container:
    ```bash
    docker run -d -p 8080:8080 -v $(pwd)/config.json:/app/config.json ghcr.io/kaiann2021/wx-notifier:main
    ```

## Usage

### 1. Send Notification
**URL**: `http://IP:8080/notify`
**Method**: `GET`
**Parameters**:
- `token`: Your `auth_token` defined in config.
- `title`: Message title (displayed as `[Title]`).
- `body`: Message content.
- `touser`: (Optional) WeCom User ID. Defaults to `@all` if omitted.

**Example**:
```
http://localhost:8080/notify?token=mysecret&title=Alert&body=Server+Down&touser=ZhangSan
```

### 2. WeCom Callback Verification
If you need to configure "API Reception" in WeCom:
- **URL**: `http://YOUR_PUBLIC_IP:8080/callback`
- **Token**: Match with `callback_token` in config.
- **EncodingAESKey**: Match with `encoding_aes_key` in config.
