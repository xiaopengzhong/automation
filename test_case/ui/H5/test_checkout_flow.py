#@File   : .py
#@Time   : 2025/9/25 19:39
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.checkout_flow import CheckoutFlow


@pytest.mark.ui
@allure.feature("结算流程")
class TestCheckoutFlow:
    @allure.story("加购并去结算")
    @allure.title("验证用户能成功从商品详情页加购并进入结算页")
    def test_checkout_success(self, driver):
        flow = CheckoutFlow(driver)
        checkout_page = flow.login_and_checkout("user001", "123456")
        assert checkout_page.is_order_success()  # 验证结算页面的标题元素存在
