#@File   : .py
#@Time   : 2025/9/23 17:56
#@Author : 
#@Software: PyCharm
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from lib.ui.web.base_page import BasePage
from lib.utils.logger import setup_logging

logger = setup_logging("ui")
class CartPage(BasePage):
    """购物车页面"""

    # 定位符
    CART_TITLE = (By.XPATH, "//div[contains(text(),'购物车')]")  # 页面标题
    TOTAL_PRICE = (By.XPATH, "//div[contains(@class,'total') or contains(text(),'¥')]")  # 商品总金额
    INCREASE_QUANTITY = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[2]//uni-view[2]/uni-text")  # 增加商品数量
    REDUCE_QUANTITY = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[2]//uni-view[1]")  # 减少商品数量
    REMOVE_PRODUCT = (By.CSS_SELECTOR, "uni-text.del-btn")  # 移除商品
    CLEAR_ITEMS_BTN = (By.XPATH, "//uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-view[2]/uni-view[1]/uni-view")  # 清空商品
    CERTAIN_CLEAR_BTN = (By.XPATH, "//uni-modal/div[2]/div[2]/div[2]")  # 确认清空
    SELECT_PRODUCT = (By.XPATH, "//uni-page-body//uni-view[1]//uni-view[1]/uni-view")  # 选中或取消选中商品
    CHECKOUT_BTN = (By.XPATH, "//uni-button[text()='去结算']")  # 去结算按钮
    EMPTY_CART_MSG = (By.XPATH, "//uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view/uni-view")  # 购物车为空
    CART_ITEMS = (By.XPATH, "//uni-page-body//uni-view[contains(@class,'cart-item')]")  # 每个商品行
    PRODUCT_QUANTITY = (By.XPATH, "//uni-page-body//uni-input//input")  # 商品数量文本框

    def __init__(self, driver):
        super().__init__(driver)

    # ---------------- 基本信息 ----------------
    def get_cart_title(self):
        """获取页面标题"""
        return self.get_text(self.CART_TITLE)

    def get_total_price(self):
        """获取商品总金额"""
        return self.get_text(self.TOTAL_PRICE).replace("¥", "").strip()

    def get_cart_items(self):
        """返回购物车中所有商品元素"""
        return self.find_elements(self.CART_ITEMS)

    def get_cart_products_count(self):
        """返回购物车商品总数"""
        return len(self.get_cart_items())

    def get_product_quantity(self, product_name=None):
        """
        获取指定商品数量（如果有多个商品，可以按商品名定位）
        """
        # 简化：直接取第一个商品的数量
        element = self.find_element(self.PRODUCT_QUANTITY)
        return int(element.get_attribute("value"))

    def wait_for_quantity_change(self, product_name, old_quantity, timeout=5):
        """等待数量元素的值更新"""
        WebDriverWait(self.driver, timeout).until(
            lambda d: self.get_product_quantity(product_name) > old_quantity
        )

    def get_cart_empty_tip(self):
        """获取购物车为空的提示"""
        return self.get_text(self.EMPTY_CART_MSG)

    def is_cart_empty(self):
        """检查购物车是否为空"""
        return self.is_element_present(self.EMPTY_CART_MSG)

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
        time.sleep(1)

    def click_clear_items(self):
        """清空商品"""
        self.click(self.CLEAR_ITEMS_BTN)
    def click_certain_clear(self):
        """确认清空"""
        self.click(self.CERTAIN_CLEAR_BTN)


    def toggle_select_product(self):
        """勾选或取消勾选商品"""
        self.click(self.SELECT_PRODUCT)

    # ---------------- 状态检查 ----------------


    def is_checkout_enabled(self):
        """检查去结算按钮是否可用"""
        return self.is_enabled(self.CHECKOUT_BTN)

    def is_product_in_cart(self, product_name):
        """检查购物车是否包含指定商品"""
        items = [item.text for item in self.get_cart_items()]  # 提取每个商品元素的文本信息，生成商品名称列表 `items`,如： ['Apple iPad 10.9英寸平板电脑 2022年款\n颜色:银色;容量:64G;\n¥3599']
        logger.info(f"items: {items}")
        return any(product_name in item for item in items)  #  使用 `any()` 判断列表中是否存在包含指定 `product_name` 的商品，返回布尔值。
