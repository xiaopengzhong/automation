#@File   : .py
#@Time   : 2025/9/25 19:35
#@Author : 
#@Software: PyCharm
import time

from lib.flows.login_flow import LoginFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.checkout_page import CheckoutPage
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.product_detail_page import ProductDetailPage
from lib.utils.logger import setup_logging

logger = setup_logging("ui")
class CheckoutFlow:
    """下单流程封装"""

    def __init__(self, driver):
        self.driver = driver

    def login_and_checkout(self, username, password, pay_now=False, remark="自动化测试订单"):
        """完整业务流：登录 → 加购 → 结算 → 提交订单 → [支付可选]"""
        # 1. 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        # 2. 浏览商品并加购
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")
        home.click_first_product()

        product_page = ProductDetailPage(self.driver)
        product_page.click_add_to_cart()
        product_page.click_go_to_cart()

        # 3. 购物车结算
        cart_page = CartPage(self.driver)
        cart_page.go_checkout()

        # 4. 提交订单
        checkout_page = CheckoutPage(self.driver)
        assert checkout_page.is_checkout_page_loaded(), "结算页加载失败"

        checkout_page.input_remark(remark)
        amount = checkout_page.get_actual_payment_amount()
        logger.info(f"实付款金额：{amount}")

        checkout_page.submit_order()

        # 5. 支付可选
        if pay_now and checkout_page.confirm_pay_popup_visible():
            checkout_page.confirm_pay()
            logger.info("订单已支付成功")
        else:
            checkout_page.cancel_pay()
            logger.info("订单未支付，取消支付弹窗")

        return checkout_page