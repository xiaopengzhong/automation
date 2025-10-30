#@File   : .py
#@Time   : 2025/10/13 0:22
#@Author : 
#@Software: PyCharm
# lib/ui/pages/mine_page.py
from selenium.webdriver.common.by import By
from lib.ui.web.base_page import BasePage

class MinePage(BasePage):
    """我的页面"""

    # ====== 定位符 ======
    USERNAME = (By.CSS_SELECTOR, ".user-name")  # 用户名
    LOGIN_BTN = (By.XPATH, "//button[contains(text(),'立即登录')]")
    ALL_ORDER_BTN = (By.XPATH, "//div[contains(text(),'全部订单')]")
    WAIT_PAY_BTN = (By.XPATH, "//div[contains(text(),'待付款')]")
    WAIT_RECEIVE_BTN = (By.XPATH, "//div[contains(text(),'待收货')]")
    REFUND_BTN = (By.XPATH, "//div[contains(text(),'退换/售后')]")
    ADDRESS_MGMT = (By.XPATH, "//div[contains(text(),'地址管理')]")
    SETTING_BTN = (By.XPATH, "//div[contains(text(),'设置')]")

    # ====== 方法 ======
    def is_mine_page_loaded(self):
        """判断‘我的’页面是否加载完成"""
        return self.is_element_present(self.ALL_ORDER_BTN)

    def get_username(self):
        """获取用户名"""
        return self.get_text_safe(self.USERNAME)

    def click_all_order(self):
        """点击全部订单"""
        self.click(self.ALL_ORDER_BTN)

    def click_wait_pay(self):
        """点击待付款"""
        self.click(self.WAIT_PAY_BTN)

    def click_wait_receive(self):
        """点击待收货"""
        self.click(self.WAIT_RECEIVE_BTN)

    def click_refund(self):
        """点击退换售后"""
        self.click(self.REFUND_BTN)

    def click_address_mgmt(self):
        """点击地址管理"""
        self.click(self.ADDRESS_MGMT)

    def click_setting(self):
        """点击设置"""
        self.click(self.SETTING_BTN)
