#@File   : .py
#@Time   : 2025/9/28 17:59
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.payment_flow import PayMentFlow


@pytest.mark.ui
@allure.feature("支付流程")
class TestPayFlow:
    @allure.story("订单支付")
    @allure.title("验证用户能支付")
    def test_pay(self, driver):
        flow = PayMentFlow(driver)
        pay_page = flow.goto_pay_page("user001", "123456")
        assert "支付" in pay_page.get_page_title()
        assert pay_page.get_order_amount() == "99.00"
        assert pay_page.is_alipay_available()
        assert pay_page.is_confirm_button_enabled()