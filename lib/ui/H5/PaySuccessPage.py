#@File   : .py
#@Time   : 2025/9/28 19:48
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


class PaySuccessPage(BasePage):
    page_title = (By.XPATH, "//uni-page/uni-page-head/div[1]/div[2]/div/text()")  # 页面标题
    check_order_btn = (By.XPATH, "//uni-page-body//uni-navigator[1]")  # 查看订单按钮
    back_home_btn = (By.XPATH, "//uni-page-body//uni-navigator[2]")  # 返回首页按钮
    def __init__(self,driver):
        super().__init__(driver)

    def get_page_title(self):
        """支付成功页面标题"""
        return self.get_text(self.page_title)
    def click_check_order_btn(self):
        """点击查看订单按钮"""
        self.click(self.check_order_btn)
    def click_back_home_btn(self):
        """点击返回首页按钮"""
        self.click(self.back_home_btn)

