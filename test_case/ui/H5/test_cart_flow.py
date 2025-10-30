#@File   : .py
#@Time   : 2025/9/23 19:20
#@Author : 
#@Software: PyCharm
import time

import pytest

from lib.flows.cart_flow import CartFlow

@pytest.mark.ui
@pytest.mark.usefixtures("driver")  # 假设你有 driver fixture
@pytest.mark.usefixtures("clean_cart")
class TestCartFlow:

    def test_add_single_product(self, driver):
        """登录后加入单个商品"""
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_single_product("user001", "123456", "iPhone")
        assert cart_page.is_product_in_cart("iPhone")

    def test_add_single_product_without_login(self, driver):
        """未登录直接加购 → 登录后成功加入"""
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_single_product_without_login("user001", "123456", "华为")
        assert cart_page.is_product_in_cart("华为")

    def test_add_multiple_products(self, driver):
        """一次性加入多个商品"""
        products = ["小米", "iPad"]
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_multiple_products("user001", "123456", products)
        for product in products:
            assert cart_page.is_product_in_cart(product)

    def test_update_cart_quantity(self, driver):
        """修改购物车数量"""
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_single_product("user001", "123456", "iPhone")
        old_qty = cart_page.get_product_quantity("iPhone")
        cart_page = cart_flow.update_cart_quantity(cart_page, action="increase")
        cart_page.wait_for_quantity_change("iPhone", old_qty)

        assert cart_page.get_product_quantity("iPhone") > old_qty

    def test_remove_product(self, driver):
        """移除商品"""
        products = ["iPhone", "iPad"]
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_multiple_products("user001", "123456", products)
        cart_page = cart_flow.remove_product(cart_page)
        assert not cart_page.is_product_in_cart("iPhone")

    def test_clear_cart(self, driver):
        """清空购物车"""
        products = ["iPhone", "iPad"]
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_multiple_products("user001", "123456", products)
        cart_page = cart_flow.clear_cart(cart_page)
        assert cart_page.get_cart_empty_tip() == "空空如也\n随便逛逛>"

    def test_go_checkout(self, driver):
        """去结算"""
        cart_flow = CartFlow(driver)
        cart_page = cart_flow.add_single_product("user001", "123456", "iPhone")
        checkout_page = cart_flow.go_checkout(cart_page)
        assert checkout_page.is_checkout_page_loaded()


