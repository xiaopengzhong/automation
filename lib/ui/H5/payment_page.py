#@File   : .py
#@Time   : 2025/9/28 16:27
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


class PayMentPage(BasePage):
    alipay_pay = (By.XPATH, "//uni-page-body//uni-view[position()=2]//uni-view[1]")  # 支付宝支付
    wechat_pay = (By.XPATH, "//uni-page-body/uni-view[2]/uni-view[2]")  # 微信支付
    confirm_pay_btn = (By.XPATH, "//uni-page-body//uni-text")  # 确认支付按钮
    payment_amount = (By.XPATH, "//uni-page-body//uni-view[1]//uni-text[2]/span")  # 支付金额
    page_title = (By.XPATH, "//uni-page-body//uni-text[contains(text(),'支付')]")  # 支付页面标题


    def __init__(self, driver):
        super().__init__(driver)

    # ---------------- 操作方法 ----------------
    def choose_alipay_pay(self):
        """选择支付宝支付"""
        self.click(self.alipay_pay)
    def choose_wechat_pay(self):
        """选择微信支付"""
        self.click(self.wechat_pay)
    def click_confirm_pay_btn(self):
        """点击确认支付"""
        self.click(self.confirm_pay_btn)

    # ---------------- 断言方法 ----------------
    def get_order_amount(self):
        """获取支付金额"""
        return self.get_text(self.payment_amount)

    def is_alipay_available(self):
        """支付宝支付方式是否可见"""
        return self.is_element_present(self.alipay_pay)

    def is_wechat_available(self):
        """微信支付方式是否可见"""
        return self.is_element_present(self.wechat_pay)

    def is_confirm_button_enabled(self):
        """确认支付按钮是否可点击"""
        return self.is_enabled(self.confirm_pay_btn)

    def get_page_title(self):
        """获取页面标题"""
        return self.get_text(self.page_title)

