#@File   : .py
#@Time   : 2025/9/24 16:43
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage



class ProductPage(BasePage):
    """商品详情页"""


    ADD_TO_CART_BTN = (By.XPATH, "//uni-view[8]/uni-view[2]/uni-button[2]")
    GO_TO_CART_BTN = (By.XPATH, "//uni-view[8]/uni-navigator[2]")

    def add_to_cart(self):
        """点击加入购物车"""
        self.click(self.ADD_TO_CART_BTN)

    def go_to_cart(self):
        """点击跳转购物车页面"""
        self.click(self.GO_TO_CART_BTN)