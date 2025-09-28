#@File   : .py
#@Time   : 2023/7/11 23:51
#@Author : 
#@Software: PyCharm
import json
import requests
from conf.env import host, phone, password, nvcVal, paas_host, paas_phone, paas_paasword, paas_nvcVal

def _post_request(url, payload, headers):
    """通用 POST 请求函数"""
    try:
        response = requests.post(url=url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as err:
        raise SystemExit(f"HTTP error occurred: {err}")
    except Exception as err:
        raise SystemExit(f"An error occurred: {err}")

def preview_login(url, phone, password, nvcVal):
    """获取预登录的 token"""
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    payload = {
        "phone": phone,
        "password": password,
        "nvcVal": nvcVal
    }
    response_data = _post_request(url, payload, headers)
    return response_data['data']['token']

def login(url, preview_token):
    """获取登录的 X-User-Token"""
    headers = {"Content-Type": "application/json;charset=UTF-8"}
    payload = {
        "companyId": 666,
        "token": preview_token,
        "appId": 51496,
        "siteId": 173688
    }
    response_data = _post_request(url, payload, headers)
    return response_data['data']['token']

# 获取应用端的token
def get_auth_tokens():
    preview_url = f"{host}/api-login/password/preview-login"
    login_url = f"{host}/api-login/login"
    preview_token = preview_login(preview_url, phone, password, nvcVal)
    return login(login_url, preview_token)
# 获取开发者端的token
def paas_get_auth_tokens():
    preview_url = f"{paas_host}/api-login/password/preview-login"
    login_url = f"{paas_host}/api-login/login"
    preview_token = preview_login(preview_url, paas_phone, paas_paasword, paas_nvcVal)
    return login(login_url, preview_token)

if __name__ == "__main__":
    # Example usage
    auth_token = get_auth_tokens()
    print(f"Auth Token: {auth_token}")

    paas_auth_token = paas_get_auth_tokens()
    print(f"PAAS Auth Token: {paas_auth_token}")
