#@File   : .py
#@Time   : 2025/9/28 17:43
#@Author : 
#@Software: PyCharm
import time

import allure

from lib.flows.login_flow import LoginFlow
from lib.ui.H5.PaySuccessPage import PaySuccessPage
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.checkout_page import CheckoutPage
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.login_page import LoginPage
from lib.ui.H5.payment_page import PayPage
from lib.ui.H5.product_page import ProductPage


class PayMentFlow:
    """下单流程封装"""

    def __init__(self, driver):
        self.driver = driver

    @allure.step("下单并跳转支付页面")
    def goto_pay_page(self,  username, password, payment_method="alipay"):
        """完整业务流：登陆 → 商品加购 → 购物车 → 结算 → 提交订单 → 支付"""
        # 1.登陆
        login_page = LoginFlow(self.driver)
        login_page.login(username, password)
        # 2. 首页浏览商品并加入购物车，并进入购物车页面
        time.sleep(2)
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")  # 返回首页
        home.click_first_product()  # 在首页点击一个商品
        # 3. 商品页操作
        product_page = ProductPage(self.driver)

        product_page.add_to_cart()
        product_page.go_to_cart()  # 点击跳转到购物车页面
        # 4. 购物车页面点击去结算
        cart_page = CartPage(self.driver)
        cart_page.go_checkout()
        # 5. 提交订单

        checkout_page = CheckoutPage(self.driver)
        checkout_page.submit_order()  # 点击提交订单
        checkout_page.go_to_pay()  # 点击去支付
        # 6.选择支付方式
        pay_page = PayPage(self.driver)
        # pay_page.choose_alipay_pay()  # 默认支付宝支付
        # pay_page.click_confirm_pay_btn()  # 点击确认支付

        return pay_page

    @allure.step("下单并支付完成")
    def pay_order(self, username, password, payment_method="alipay"):
        """完整下单支付流程，返回支付成功页面 PaySuccessPage"""
        pay_page = self.goto_pay_page(username, password)

        # 选择支付方式
        if payment_method.lower() == "alipay" and pay_page.is_alipay_available():
            pay_page.choose_alipay_pay()
        elif payment_method.lower() == "wechat" and pay_page.is_wechat_available():
            pay_page.choose_wechat_pay()
        else:
            raise Exception(f"支付方式不可用: {payment_method}")

        # 点击确认支付
        pay_page.click_confirm_pay_btn()
        # 7. 返回支付成功页面对象
        success_page = PaySuccessPage(self.driver)
        return success_page


