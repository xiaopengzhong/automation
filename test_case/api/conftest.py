# @File   : .py
# @Time   : 2023/7/23 22:44
# @Author :
# @Software: PyCharm
import pytest

from lib.api.user.cart import CartAPI
from lib.api.user.login import LoginAPI


@pytest.fixture(autouse=True)
def clean_cart():
    """每个用例前后清空购物车，保证环境幂等"""
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get("auth_token")
    CartAPI(token, payload_file="case_data/api/user/payload.yaml").clear_cart()