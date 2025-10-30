#@File   : test_cart.py
#@Time   : 2025/10/21 1:32
#@Author :
#@Software: PyCharm

import pytest
import allure
from lib.api.user.cart import CartAPI
from lib.api.user.login import LoginAPI
from lib.utils.config_loader import load_yaml
from lib.utils.logger import setup_logging

logger = setup_logging("api")





@pytest.fixture(scope="class")
def cart_api():
    """登录态购物车接口实例"""
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get("auth_token")
    return CartAPI(token, payload_file="case_data/api/user/payload.yaml")


@pytest.fixture(scope="class")
def no_login_cart_api():
    """未登录购物车接口实例"""
    return CartAPI(token=None, payload_file="case_data/api/user/payload.yaml")


@pytest.mark.api
@allure.feature("购物车模块")
class TestCartAPI:
    """购物车模块测试"""

    # ✅ 添加购物车
    @allure.story("添加商品到购物车")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/cart.yaml")["add_cart"])
    def test_add_cart(self, data, cart_api):
        logger.info(f"🧩 开始执行用例：[{data.get('id', '')}] {data['desc']}")
        expected = data["expected"]

        with allure.step("发起添加购物车请求"):
            resp = cart_api.add_cart(**data["data"])

        with allure.step("断言响应结果"):
            assert resp["code"] == expected["code"], f"状态码错误 -> 实际:{resp['code']} 期望:{expected['code']}"
            assert expected["message"] in resp["message"], f"消息断言失败 -> 实际:{resp['message']}"
            if "data" in expected:
                assert resp["data"] == expected["data"], f"返回 data 不匹配 -> {resp['data']}"

    # ✅ 查看购物车列表
    @allure.story("查看购物车列表")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/cart.yaml")["list_cart"])
    def test_list_cart(self, data, cart_api, no_login_cart_api):
        logger.info(f"🧩 开始执行用例：[{data.get('id', '')}] {data['desc']}")
        expected = data["expected"]

        # 处理前置条件
        pre = data.get("precondition", "")
        if "清空" in pre:
            logger.info("前置条件：清空购物车")
            cart_api.clear_cart()
            api = cart_api
        elif "添加" in pre:
            logger.info("前置条件：添加两件商品到购物车")
            cart_api.clear_cart()
            cart_api.add_cart(productId=38, quantity=1)
            cart_api.add_cart(productId=29, quantity=1)
            api = cart_api
        elif "未登录" in pre:
            logger.info("前置条件：使用未登录接口实例")
            api = no_login_cart_api
        else:
            api = cart_api

        with allure.step(f"执行场景：{data.get('desc', '')}"):
            try:
                resp = api.list_cart()
            except Exception as e:
                logger.error(f"接口调用异常：{e}")
                pytest.fail(f"接口请求失败：{e}")

        with allure.step("断言响应结果"):
            assert str(resp.get("code")) == str(expected["code"]), f"状态码错误 -> {resp}"
            if "message" in expected:
                assert expected["message"] in resp.get("message", ""), f"消息断言失败 -> {resp}"

            # 未登录场景
            if resp.get("code") == 401:
                logger.info("验证未登录场景响应")
                assert resp.get("message") in [
                    "暂未登录或token已经过期",
                    "Full authentication is required to access this resource"
                ], f"未登录提示不符 -> {resp.get('message')}"
                assert isinstance(resp.get("data"), str), "未登录时 data 应为错误信息字符串"
                return

            # 登录成功场景
            cart_items = resp.get("data", [])
            assert isinstance(cart_items, list), f"data 应为 list，实际为 {type(cart_items).__name__}"

            if expected.get("empty"):
                assert cart_items == [], "购物车应为空"
                return

            if expected.get("contain_field"):
                first = cart_items[0]
                for field in expected["contain_field"]:
                    assert field in first, f"字段缺失：{field}"

            if expected.get("contain_value"):
                first = cart_items[0]
                found = any(v in str(first.values()) for v in expected["contain_value"])
                assert found, f"未找到期望值 {expected['contain_value']}"

            if expected.get("item_count_gt"):
                assert len(cart_items) > expected["item_count_gt"], f"期望数量 > {expected['item_count_gt']}"
            elif expected.get("item_count_ge"):
                assert len(cart_items) >= expected["item_count_ge"], f"期望数量 ≥ {expected['item_count_ge']}"

    # ✅ 更新数量
    @allure.story("更新购物车商品数量")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/cart.yaml")["update_quantity_cart"])
    def test_update_quantity_cart(self, data, cart_api, no_login_cart_api):
        logger.info(f"🧩 开始执行用例：[{data.get('id', '')}] {data['desc']}")
        expected = data["expected"]

        precondition = data.get("precondition", "")
        if "未登录" in precondition:
            api = no_login_cart_api
        else:
            api = cart_api
            # 正常场景准备购物车项
            if not precondition or "非法ID" not in precondition:
                api.add_cart(productId=38, quantity=1)
                item_id = api.list_cart()["data"][0]["id"]
                data["data"]["id"] = item_id

        resp = api.update_quantity_cart(**data["data"])

        assert str(resp.get("code")) == str(expected["code"]), f"状态码错误 -> {resp}"
        assert expected["message"] in resp.get("message", ""), f"消息断言失败 -> {resp}"

    # ✅ 删除购物车商品
    @allure.story("删除购物车商品")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/cart.yaml")["delete_cart"])
    def test_delete_cart(self, data, cart_api, no_login_cart_api):
        logger.info(f"🧩 开始执行用例：[{data.get('id', '')}] {data['desc']}")
        expected = data["expected"]

        precondition = data.get("precondition", "")
        if "未登录" in precondition:
            api = no_login_cart_api
        else:
            api = cart_api
            # 正常场景先添加商品
            if not precondition or "不存在" not in precondition:
                api.add_cart(productId=38, quantity=1)
                item_id = api.list_cart()["data"][0]["id"]
                data["data"]["ids"] = str(item_id)

        resp = api.delete_cart(**data["data"])

        assert str(resp.get("code")) == str(expected["code"]), f"状态码错误 -> {resp}"
        assert expected["message"] in resp.get("message", ""), f"消息断言失败 -> {resp}"

        if resp.get("code") == 200:
            cart_data = api.list_cart().get("data", [])
            assert cart_data == [], "删除后购物车应为空"

    # ✅ 清空购物车
    @allure.story("清空购物车")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/cart.yaml")["clear_cart"])
    def test_clear_cart(self, data, cart_api, no_login_cart_api):
        logger.info(f"🧩 开始执行用例：[{data.get('id', '')}] {data['desc']}")
        expected = data["expected"]

        precondition = data.get("precondition", "")
        if "未登录" in precondition:
            api = no_login_cart_api
        else:
            api = cart_api
            api.add_cart(productId=38, quantity=1)

        resp = api.clear_cart()

        assert str(resp.get("code")) == str(expected["code"]), f"状态码错误 -> {resp}"
        assert expected["message"] in resp.get("message", ""), f"消息断言失败 -> {resp}"

        if resp.get("code") == 200:
            cart_data = api.list_cart().get("data", [])
            assert cart_data == [], "清空后购物车应为空"

