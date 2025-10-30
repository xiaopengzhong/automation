#@File   : .py
#@Time   : 2025/10/21 23:47
#@Author : 
#@Software: PyCharm
# test_case/test_auth.py
import pytest
import allure
from lib.auth import AuthAPI

from lib.api.user.login import LoginAPI
from lib.utils.config_loader import load_yaml


@allure.story("登录接口")
@pytest.mark.parametrize("data", load_yaml("case_data/api/user/login.yaml")["login"])
def test_login(self, data):
    """验证登录接口"""
    username = data["username"]
    password = data["password"]
    expected_status = data["expected_status"]
    expected_message = data.get("expected_message")
    allure.dynamic.title(f"登录测试 - {username}")

    auth_api = LoginAPI()
    with allure.step(f"执行登录: 用户名 {username}"):
        try:
            token = auth_api.login(username=username, password=password)
            assert expected_status == 200, "登录应成功"
            assert token is not None, "应返回有效 token"
        except ValueError as e:
            response = e.__context__.response
            assert response.status_code == expected_status, f"状态码不符，预期: {expected_status}, 实际: {response.status_code}"
            if expected_message:
                assert response.json().get("message") == expected_message, f"消息不符，预期: {expected_message}"