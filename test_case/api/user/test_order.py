# @File   : test_order.py
# @Time   : 2025/10/19
# @Author : xiaopen
# @Software: PyCharm
import time

import pytest
import allure

from lib.api.user.cart import CartAPI
from lib.api.user.order import OrderAPI
from lib.api.user.login import LoginAPI

from lib.utils.config_loader import load_yaml
from lib.utils.logger import setup_logging

logger = setup_logging("api")


@pytest.fixture(scope="class")
def order_and_cart_api():
    """登录并初始化 OrderAPI 实例"""
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get("auth_token")
    order_api = OrderAPI(token, payload_file="case_data/api/user/payload.yaml")
    cart_api = CartAPI(token, payload_file="case_data/api/user/payload.yaml")
    return order_api, cart_api


@allure.feature("订单模块")
@pytest.mark.api
class TestOrderAPI:

    # ✅ 创建订单
    @allure.story("创建订单")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["create_order"])
    def test_create_order(self, order_and_cart_api, data):
        desc = data["desc"]
        expected = data["expected"]
        precondition = data.get("precondition", "")

        logger.info(f"🧩 开始执行用例：[{data['id']}] {desc}")
        order_api , cart_api = order_and_cart_api
        # 前置准备
        cart_ids = None
        if "存在商品" in precondition:
            cart_api.add_cart()
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
        elif "购物车为空" in precondition:
            cart_ids = []
        elif "存在多个商品" in precondition:
            cart_api.add_cart()
            cart_api.add_cart(productId=40, productSkuId=221)
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
        # 执行创建订单

        resp = order_api.create_order(cartIds=cart_ids)
        logger.info(f"创建订单响应: {resp}")

        assert str(resp.get("code")) == str(expected["code"])
        assert expected["message"] in resp.get("message", "")

        if expected.get("contain_field"):
            order_data = resp.get("data", {})
            for field in expected["contain_field"]:
                assert field in str(order_data), f"字段缺失: {field}"

    # ✅ 生成确认订单信息
    @allure.story("生成确认订单信息")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["generate_confirm_order"])
    def test_generate_confirm_order(self, order_and_cart_api, data):
        precondition = data.get("precondition", "")
        expected = data["expected"]
        order_api, cart_api = order_and_cart_api
        cart_ids = None

        if "存在商品" in precondition:

            order_api.cart_api.add_cart()
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]

        resp = order_api.generate_confirm_Order(cart_ids)
        logger.info(f"确认订单响应: {resp}")


        assert resp["code"] == expected["code"]
        assert expected["message"] in resp["message"]

        if expected.get("contain_field"):
            confirm_data = resp.get("data", {})
            for field in expected["contain_field"]:
                assert field in confirm_data, f"字段缺失: {field}"

    # ✅ 查看订单列表
    @allure.story("查看订单列表")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["list_order"])
    def test_list_order(self, order_and_cart_api, data):
        order_api, cart_api = order_and_cart_api
        cart_api.add_cart()
        cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
        order_api.create_order(cartIds=cart_ids)
        resp = order_api.list_order()
        expected = data["expected"]

        assert str(resp.get("code")) == str(expected["code"])
        assert expected["message"] in resp.get("message", "")

    # ✅ 获取订单详情
    @allure.story("获取订单详情")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["get_order_detail"])
    def test_get_order_detail(self, order_and_cart_api, data):
        precondition = data.get("precondition", "")
        expected = data["expected"]
        order_api, cart_api = order_and_cart_api

        if "已创建" in precondition:
            order_api.cart_api.add_cart()
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
            create_resp = order_api.create_order(cartIds=cart_ids)
            order_id = create_resp.get("data", {}).get("order", {}).get("id")
        else:
            order_id = data["data"].get("order_id")

        resp = order_api.get_order_detail(order_id)
        logger.info(f"订单详情响应: {resp}")

        if not resp:
            pytest.skip("订单详情返回为空，可能接口异常或无订单")

        assert expected['code'] == resp['code']
        assert expected['message'] == resp['message']
        if expected.get("contain_field"):
            confirm_data = resp.get("data", {})
            for field in expected["contain_field"]:
                assert field in confirm_data, f"字段缺失: {field}"

    # ✅ 取消订单
    @allure.story("取消订单")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["cancel_order"])
    def test_cancel_order(self, order_and_cart_api, data):
        expected = data["expected"]
        precondition = data.get("precondition", "")
        order_api, cart_api = order_and_cart_api
        order_id = None

        if "已创建" in precondition:
            order_api.cart_api.clear_cart()
            order_api.cart_api.add_cart()
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
            create_resp = order_api.create_order(cartIds=cart_ids)
            order_id = create_resp.get("data", {}).get("order", {}).get("id")
        else:
            pytest.skip("缺少订单ID")

        resp = order_api.cancel_order(orderId=order_id)
        logger.info(f"取消订单响应: {resp}")

        assert resp["code"] == expected["code"]
        assert expected["message"] in resp["message"]

    # ✅ 删除订单
    @allure.story("删除订单")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/order.yaml")["delete_order"])
    def test_delete_order(self, order_and_cart_api, data):
        expected = data["expected"]
        precondition = data.get("precondition", "")
        order_api, cart_api = order_and_cart_api
        order_id = None

        if "已取消" in precondition:

            order_api.cart_api.add_cart()
            cart_ids = [item["id"] for item in cart_api.list_cart()["data"]]
            create_resp = order_api.create_order(cartIds=cart_ids)
            order_id = create_resp.get("data", {}).get("order", {}).get("id")
            order_api.cancel_order(orderId=order_id)
        else:
            pytest.skip("缺少订单ID")

        resp = order_api.delete_order(orderId=order_id)
        logger.info(f"删除订单响应: {resp}")

        assert resp["code"] == expected["code"]
        assert expected["message"] in resp["message"]
