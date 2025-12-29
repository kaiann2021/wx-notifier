import requests
import time
import json

class WeComClient:
    def __init__(self, corpid, corpsecret, agentid):
        self.corpid = corpid
        self.corpsecret = corpsecret
        self.agentid = agentid
        self.access_token = None
        self.token_expires_at = 0

    def _get_access_token(self):
        # Buffer of 60 seconds to be safe
        if self.access_token and time.time() < self.token_expires_at - 60:
            return self.access_token

        url = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.corpid}&corpsecret={self.corpsecret}"
        try:
            response = requests.get(url)
            data = response.json()
            if data.get("errcode") == 0:
                self.access_token = data.get("access_token")
                expires_in = data.get("expires_in", 7200)
                self.token_expires_at = time.time() + expires_in
                return self.access_token
            else:
                print(f"Error fetching access token: {data}")
                return None
        except Exception as e:
            print(f"Exception fetching access token: {e}")
            return None

    def send_text(self, title, body, touser="@all"):
        token = self._get_access_token()
        if not token:
            return {"errcode": -1, "errmsg": "Failed to get access token"}

        url = f"https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}"
        
        # Using Text message type.
        # Format: [Title]
        #         Body
        content = ""
        if title:
            content += f"[{title}]\n"
        content += body

        payload = {
            "touser": touser,
            "msgtype": "text",
            "agentid": self.agentid,
            "text": {
                "content": content
            },
            "safe": 0
        }

        try:
            response = requests.post(url, json=payload)
            return response.json()
        except Exception as e:
            return {"errcode": -2, "errmsg": f"Exception sending message: {e}"}
