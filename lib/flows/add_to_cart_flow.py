#@File   : .py
#@Time   : 2025/9/29 0:42
#@Author : 
#@Software: PyCharm
from lib.flows.login_flow import LoginFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.product_page import ProductPage


class CartFlow:
    """购物车业务流程"""

    def __init__(self, driver):
        self.driver = driver

    def add_single_product(self, username, password, product_name=None):
        """
        登录 → 浏览商品 → 加入购物车 → 打开购物车
        """
        # 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        # 打开首页
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")

        # 点击首页第一个商品（或指定商品）
        if product_name:
            home.search_product(product_name)
            home.click_first_product()
        else:
            home.click_first_product()

        # 商品页操作
        product_page = ProductPage(self.driver)
        product_page.add_to_cart()
        product_page.go_to_cart()

        return CartPage(self.driver)

    def add_multiple_products(self, username, password, products):
        """
        登录 → 加入多个商品到购物车
        :param products: 商品名列表，如 ["iPhone", "华为手机"]
        """
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        home = HomePage(self.driver)

        for product in products:
            home.open_url("http://localhost:8060/#/")
            home.search_product(product)
            home.click_first_product()
            product_page = ProductPage(self.driver)
            product_page.add_to_cart()

        # 最后进入购物车
        product_page.go_to_cart()
        return CartPage(self.driver)

    def update_cart_quantity(self, cart_page, action="increase"):
        """
        修改购物车中商品数量
        :param action: "increase" 或 "reduce"
        """
        if action == "increase":
            cart_page.click_increase_quantity()
        elif action == "reduce":
            cart_page.click_reduce_quantity()
        else:
            raise ValueError("action 只能是 'increase' 或 'reduce'")
        return cart_page

    def remove_product(self, cart_page):
        """移除单个商品"""
        cart_page.click_remove_product()
        return cart_page

    def clear_cart(self, cart_page):
        """清空购物车"""
        cart_page.click_clear_items()
        return cart_page

    def go_checkout(self, cart_page):
        """去结算"""
        cart_page.go_checkout()
        return cart_page