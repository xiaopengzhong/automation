#@File   : .py
#@Time   : 2025/10/3 15:00
#@Author : 
#@Software: PyCharm

# lib/api/user/login_api.py


from lib.api.user.baseAPI import BaseAPI

import copy
class LoginAPI(BaseAPI):
    def __init__(self, payload_file=None):
        super().__init__(payload_file=payload_file)

    def login(self, **kwargs):
        """
        用户登录，自动拼接鉴权 Token
        Returns:
            dict: {
                "status_code": int,
                "elapsed_time": float,
                "body": dict,
                "auth_token": str|None
            }
        """
        url = "/sso/login"

        # 拿到默认 payload
        payload = copy.deepcopy(self.payload.get("login_param", {}))
        payload.update(kwargs)
        # 发送请求
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        resp = self.post(endpoint=url, data=payload, headers=headers)
        # 将 Response 转为 dict
        try:
            body = resp.json()
        except Exception:
            body = {"raw_text": resp.text}

        # 提取 token
        auth_token = None
        if isinstance(body, dict) and "data" in body:
            data = body["data"]
            token_head = data.get("tokenHead", "")
            token = data.get("token", "")
            if token_head and token:
                auth_token = f"{token_head}{token}"

        # 返回统一结构
        result = {
            "status_code": resp.status_code,
            "elapsed_time": resp.elapsed.total_seconds(), #  获取 HTTP 请求的响应耗时，单位是秒（浮点数）
            "body": body,
            "auth_token": auth_token
        }
        return result


if __name__ == "__main__":
    api = LoginAPI(payload_file="../../../case_data/api/user/payload.yaml")
    result = api.login()
    print("完整响应:", result)
    print("拼接后的 Token:", result["auth_token"])
