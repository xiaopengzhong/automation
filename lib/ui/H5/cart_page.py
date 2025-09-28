#@File   : .py
#@Time   : 2025/9/23 17:56
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By
from lib.ui.web.base_page import BasePage


class CartPage(BasePage):
    """购物车页面"""

    # 定位符
    CART_TITLE = (By.XPATH, "//div[contains(text(),'购物车')]")  # 页面标题
    TOTAL_PRICE = (By.XPATH, "//div[contains(@class,'total') or contains(text(),'¥')]")  # 商品总金额
    INCREASE_QUANTITY = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[2]//uni-view[2]/uni-text")  # 增加商品数量
    REDUCE_QUANTITY = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[2]//uni-view[1]")  # 减少商品数量
    REMOVE_PRODUCT = (By.XPATH, "//uni-page-body//uni-view[1]//uni-text")  # 移除商品
    CLEAR_ITEMS = (By.XPATH, "//uni-page-body//uni-view[2]//uni-view[1]/uni-view")  # 清空商品
    SELECT_PRODUCT = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[1]/uni-view")  # 选中或取消选中商品
    CHECKOUT_BTN = (By.XPATH, "//uni-button[text()='去结算']")  # 去结算按钮
    EMPTY_CART_MSG = (By.XPATH, "//div[contains(text(),'空') or contains(text(),'购物车为空')]")  # 购物车为空
    CART_ITEMS = (By.XPATH, "//uni-page-body//uni-view[contains(@class,'cart-item')]")  # 每个商品行

    def __init__(self, driver):
        super().__init__(driver)

    # ---------------- 基本信息 ----------------
    def get_cart_title(self):
        """获取页面标题"""
        return self.get_text(self.CART_TITLE)

    def get_total_price(self):
        """获取商品总金额"""
        return self.get_text(self.TOTAL_PRICE)

    def get_cart_items(self):
        """返回购物车中所有商品元素"""
        return self.find_elements(self.CART_ITEMS)

    def get_cart_items_count(self):
        """返回购物车商品数量"""
        return len(self.get_cart_items())

    # ---------------- 操作 ----------------
    def go_checkout(self):
        """点击去结算按钮"""
        self.click(self.CHECKOUT_BTN)

    def click_increase_quantity(self):
        """增加商品数量"""
        self.click(self.INCREASE_QUANTITY)

    def click_reduce_quantity(self):
        """减少商品数量"""
        self.click(self.REDUCE_QUANTITY)

    def click_remove_product(self):
        """移除商品"""
        self.click(self.REMOVE_PRODUCT)

    def click_clear_items(self):
        """清空商品"""
        self.click(self.CLEAR_ITEMS)

    def toggle_select_product(self):
        """勾选或取消勾选商品"""
        self.click(self.SELECT_PRODUCT)

    # ---------------- 状态检查 ----------------
    def is_cart_empty(self):
        """检查购物车是否为空"""
        return self.is_element_present(self.EMPTY_CART_MSG)

    def is_checkout_enabled(self):
        """检查去结算按钮是否可用"""
        return self.is_enabled(self.CHECKOUT_BTN)

    def has_product(self, product_name):
        """检查购物车是否包含指定商品"""
        items = [item.text for item in self.get_cart_items()]
        return any(product_name in item for item in items)
