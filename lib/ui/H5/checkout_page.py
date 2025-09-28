#@File   : .py
#@Time   : 2025/9/25 19:06
#@Author : 
#@Software: PyCharmfrom lib.ui.base_page import BasePage
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


class CheckoutPage(BasePage):
    """结算页"""


    confirm_order_text = (By.XPATH, "//uni-page-head/div[1]/div[2]/div")
    submit_order_button = (By.XPATH, "//uni-page-body/uni-view/uni-view[4]/uni-text")  # 提交订单按钮
    pay_btn = (By.XPATH, "//uni-app/uni-modal/div[2]/div[3]/div[2]")  # 支付按钮
    cannel_pay_btn = (By.XPATH, "//uni-app/uni-modal/div[2]/div[3]/div[1]")  # 取消支付按钮
    def __init__(self,driver):
        super().__init__(driver)

    def is_order_success(self):
        """检查结算页是否加载成功"""
        return self.is_element_present(self.confirm_order_text)

    def submit_order(self):
        """点击提交订单按钮"""
        self.click(self.submit_order_button)
    def go_to_pay(self):
        """点击去支付"""
        self.click(self.pay_btn)

    def cannel_pay(self):
        """点击取消支付"""
        self.click(self.cannel_pay_btn)


