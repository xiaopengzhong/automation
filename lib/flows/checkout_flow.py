#@File   : .py
#@Time   : 2025/9/25 19:35
#@Author : 
#@Software: PyCharm
import time

from lib.flows.login_flow import LoginFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.checkout_page import CheckoutPage
from lib.ui.H5.home_page import HomePage

from lib.ui.H5.product_page import ProductPage


class CheckoutFlow:
    """下单流程封装"""

    def __init__(self, driver):
        self.driver = driver

    def login_and_checkout(self,  username, password):
        """完整业务流：登陆 → 商品加购 → 购物车 → 结算 → 提交订单"""
        # 1.登陆
        login_page = LoginFlow(self.driver)
        login_page.login(username, password)
        # 2. 浏览商品并加入购物车，并进入购物车页面

        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")  # 返回首页
        home.click_first_product()  # 在首页点击一个商品

        product_page = ProductPage(self.driver)

        product_page.add_to_cart()
        product_page.go_to_cart()  # 点击跳转到购物车页面
        # 3. 购物车页面点击去结算
        cart_page = CartPage(self.driver)
        cart_page.go_checkout()
        # 4. 提交订单

        checkout_page = CheckoutPage(self.driver)


        return checkout_page


