#@File   : .py
#@Time   : 2025/9/29 2:40
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.search_product_flow import SearchProductFlow

@pytest.mark.ui
@allure.feature("搜索商品流程")
class TestSearchProductFlow:
    @allure.story("搜索商品")
    @allure.title("搜索商品成功")
    def test_search_product_success(self, driver):
        flow = SearchProductFlow(driver)
        search_page = flow.search_product("test_user", "123456", "iPhone")
        assert len(search_page.get_product_items()) > 0
        assert "iPhone" in search_page.get_first_product_info()

    @allure.story("搜索商品")
    @allure.title("搜索商品失败")
    def test_search_product_empty(self, driver):
        flow = SearchProductFlow(driver)
        search_page = flow.search_product("test_user", "123456", "不存在的商品XYZ")
        assert search_page.is_empty_result()
