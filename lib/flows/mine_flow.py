#@File   : .py
#@Time   : 2025/10/13 0:22
#@Author : 
#@Software: PyCharm
# lib/ui/flows/mine_flow.py
from lib.ui.H5.mine_page import MinePage
from lib.ui.H5.order_list_page import OrderListPage


class MineFlow:
    """‘我的’页面业务流"""

    def __init__(self, driver):
        self.driver = driver

    def open_my_orders(self):
        """进入订单列表页"""
        mine_page = MinePage(self.driver)
        assert mine_page.is_mine_page_loaded(), "‘我的’页面未加载完成"
        mine_page.click_all_order()
        order_page = OrderListPage(self.driver)
        assert order_page.is_order_page_loaded(), "订单列表页加载失败"
        return order_page

    def check_login_user(self):
        """获取当前登录用户名"""
        mine_page = MinePage(self.driver)
        assert mine_page.is_mine_page_loaded(), "‘我的’页面未加载完成"
        return mine_page.get_username()
