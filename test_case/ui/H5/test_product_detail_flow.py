#@File   : .py
#@Time   : 2025/9/29 23:43
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.product_detail_flow import ProductDetailFlow


@pytest.mark.ui
@allure.feature("商品详情")
class TestProductDetail:
    @allure.story("查看商品详情")
    @allure.title("验证商品详情信息")
    def test_view_product_detail(self, driver):
        flow = ProductDetailFlow(driver)
        product_page = flow.view_product(
            username="user001",
            password="123456",
            keyword="华为",
        )

        # 断言商品详情页标题和价格
        title = product_page.get_product_title()
        price = product_page.get_product_price()

        assert title != ""
        assert price != ""