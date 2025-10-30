#@File   : .py
#@Time   : 2025/10/12 16:20
#@Author : 
#@Software: PyCharm

from lib.ui.H5.order_detail_page import OrderDetailPage
from lib.ui.H5.order_list_page import OrderListPage


# lib/ui/flows/order_detail_flow.py


class OrderDetailFlow:
    """订单详情业务流"""

    def __init__(self, driver):
        self.driver = driver

    def open_first_order_detail(self):
        """从订单列表页进入订单详情页"""
        order_list_page = OrderListPage(self.driver)
        order_list_page.click_first_order()
        order_detail_page = OrderDetailPage(self.driver)
        assert order_detail_page.is_order_detail_loaded(), "订单详情页未加载完成"
        return order_detail_page

    def get_order_detail_info(self):
        """获取订单详情信息"""
        order_detail_page = self.open_first_order_detail()
        return order_detail_page.get_order_detail()
