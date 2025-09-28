#@File   : .py
#@Time   : 2025/9/23 19:20
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.add_to_cart_flow import AddToCartFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.product_page import ProductPage


@pytest.mark.ui
@allure.feature("购物车模块")
class TestCart:
    @allure.story("添加商品到购物车并结算")
    @allure.title("验证加入购物车后可以去结算")
    def test_add_to_cart_and_checkout(self, driver):
        flow = AddToCartFlow(driver)
        cart_page = flow.add_to_cart("test_user", "123456", "华为手机")

        assert cart_page.get_cart_items_count() > 0
        assert cart_page.has_product("华为手机")
        assert cart_page.is_checkout_enabled()