#@File   : .py
#@Time   : 2025/9/29 0:42
#@Author : 
#@Software: PyCharm
from lib.flows.login_flow import LoginFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.checkout_page import CheckoutPage
from lib.ui.H5.home_page import HomePage


from lib.ui.H5.product_detail_page import ProductDetailPage
from lib.ui.H5.product_search_page import ProducSearchtPage


class CartFlow:
    """购物车业务流程"""

    def __init__(self, driver):
        self.driver = driver

    def _search_and_open_product(self, product_name):
        """通用步骤：从首页搜索商品并进入详情页"""
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")  # 进入首页
        home.click_search_input()  # 点击搜索框进入搜索页面

        search_product_page = ProducSearchtPage(self.driver)
        search_product_page.set_enter_product_name(product_name)
        search_product_page.click_search_btn()
        search_product_page.click_product()

        return ProductDetailPage(self.driver)

    def add_single_product(self, username, password, product_name):
        """登录后加入单个商品到购物车"""
        # 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        # 搜索并进入详情页
        product_detail_page = self._search_and_open_product(product_name)

        # 加入购物车
        product_detail_page.click_add_to_cart()
        product_detail_page.click_go_to_cart()

        return CartPage(self.driver)

    def add_single_product_without_login(self, username, password, product_name):
        """未登录直接加购 → 提示登录 → 登录后再加购"""
        product_detail_page = self._search_and_open_product(product_name)

        # 点击加入购物车（未登录会跳登录）
        product_detail_page.click_add_to_cart()
        product_detail_page.click_go_to_login()

        # 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password, open_page=False)

        # 再次加购并进入购物车
        product_detail_page.click_add_to_cart()
        product_detail_page.click_go_to_cart()

        return CartPage(self.driver)

    def add_multiple_products(self, username, password, products):
        """一次性加入多个商品"""
        global product_detail_page
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        for product_name in products:
            product_detail_page = self._search_and_open_product(product_name)
            product_detail_page.click_add_to_cart()

        # 最后进入购物车
        product_detail_page.click_go_to_cart()
        return CartPage(self.driver)

    def update_cart_quantity(self, cart_page, action="increase"):
        """修改购物车中商品数量"""
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
        cart_page.click_certain_clear()
        return cart_page

    def go_checkout(self, cart_page):
        """去结算"""
        cart_page.go_checkout()
        return CheckoutPage(self.driver)
