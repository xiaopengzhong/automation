#@File   : .py
#@Time   : 2025/9/29 2:06
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


from selenium.webdriver.common.by import By
from lib.ui.web.base_page import BasePage


class SearchProductPage(BasePage):
    """商品搜索页"""

    # 定位符
    ENTER_PRODUCT_NAME = (By.XPATH, "//uni-page-body//uni-input//input")  # 输入商品名称
    SEARCH_BTN = (By.XPATH, "//uni-page-body//uni-button")  # 搜索按钮
    PRODUCT_INFORMATION = (By.XPATH, "//uni-scroll-view//uni-view[1]//uni-text[1]/span")  # 第一个商品信息
    PRODUCT_DESCRIPTION = (By.XPATH, "//uni-scroll-view//uni-view[1]//uni-text[2]/span")  # 第一个商品描述
    PRODUCT_ITEMS = (By.XPATH, "//uni-scroll-view//div/div/div")  # 搜索结果商品集合
    EMPTY_PRODUCT = (By.XPATH, "//div[contains(text(),'没有找到') or contains(text(),'暂无商品')]")  # 搜索无结果提示

    def set_enter_product_name(self, product_name):
        """输入商品名称"""
        self.send_keys(self.ENTER_PRODUCT_NAME, product_name)

    def click_search_btn(self):
        """点击搜索按钮"""
        self.click(self.SEARCH_BTN)

    def get_first_product_info(self):
        """获取第一个商品标题"""
        return self.get_text(self.PRODUCT_INFORMATION)

    def get_first_product_description(self):
        """获取第一个商品描述"""
        return self.get_text(self.PRODUCT_DESCRIPTION)

    def get_product_items(self):
        """获取搜索结果商品集合"""
        return self.find_elements(self.PRODUCT_ITEMS)

    def is_empty_result(self):
        """判断是否搜索为空"""
        return self.is_element_present(self.EMPTY_PRODUCT)
