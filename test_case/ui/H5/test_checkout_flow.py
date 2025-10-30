#@File   : .py
#@Time   : 2025/9/25 19:39
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.flows.checkout_flow import CheckoutFlow


@pytest.mark.ui
@allure.feature("结算流程")
@pytest.mark.usefixtures("driver")
class TestCheckoutFlow:

    def test_checkout_order_create(self, driver):
        """验证下单流程：登录→加购→结算→提交订单"""
        checkout_flow = CheckoutFlow(driver)
        checkout_page = checkout_flow.login_and_checkout(
            username="user001",
            password="123456",
            pay_now=False
        )
        assert checkout_page.is_checkout_page_loaded(), "结算页加载失败"
        amount = checkout_page.get_actual_payment_amount()
        assert amount and amount > 0, "实付款金额应大于0"

    def test_checkout_and_pay(self, driver):
        """验证下单并支付流程"""
        checkout_flow = CheckoutFlow(driver)
        checkout_page = checkout_flow.login_and_checkout(
            username="user001",
            password="123456",
            pay_now=True
        )
        assert not checkout_page.confirm_pay_popup_visible(), "支付弹窗未关闭，支付失败"