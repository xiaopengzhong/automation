#@File   : .py
#@Time   : 2025/10/5 17:16
#@Author : 
#@Software: PyCharm
# lib/ui/pages/order_list_page.py
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


class OrderListPage(BasePage):
    """订单列表页（我的订单）"""

    # ==== 定位符 ====
    all_tab = (By.XPATH, "//uni-page-body//uni-view[1][text()='全部']")
    wait_pay_tab = (By.XPATH, "//uni-page-body//uni-view[2][text()='待付款']")
    wait_receive_tab = (By.XPATH, "//uni-page-body//uni-view[3][text()='待收货']")
    completed_tab = (By.XPATH, "//uni-page-body//uni-view[4][text()='已完成']")
    cancelled_tab = (By.XPATH, "//uni-page-body//uni-view[5][text()='已取消']")

    first_order_card = (By.CSS_SELECTOR, "uni-text.time")
    first_order_status = (By.XPATH, "//uni-swiper-item[1]//uni-text[2]/span")
    first_order_amount = (By.CSS_SELECTOR, "uni-text.price")
    first_order_name = (By.CSS_SELECTOR, "uni-text.title.clamp")
    first_order_time = (By.CSS_SELECTOR, "uni-text.time")

    def __init__(self, driver):
        super().__init__(driver)

    # ==== 页面行为 ====
    def is_order_page_loaded(self):
        """判断订单列表页是否加载完成"""
        return self.is_element_present(self.all_tab)

    def switch_tab(self, tab_name):
        """切换订单状态标签页"""
        tabs = {
            "全部": self.all_tab,
            "待付款": self.wait_pay_tab,
            "待收货": self.wait_receive_tab,
            "已完成": self.completed_tab,
            "已取消": self.cancelled_tab,
        }
        if tab_name not in tabs:
            raise ValueError(f"未知的订单标签: {tab_name}")
        self.click(tabs[tab_name])

    def get_first_order_info(self):
        """获取订单列表中第一条订单信息"""
        name = self.get_text(self.first_order_name)
        status = self.get_text(self.first_order_status)
        amount = self.get_text_with_before(self.first_order_amount)
        order_time = self.get_text(self.first_order_time)
        return {
            "name": name,
            "status": status,
            "amount": amount,
            "order_time": order_time
        }

    def click_first_order(self):
        """点击进入订单详情"""
        self.click(self.first_order_card)


