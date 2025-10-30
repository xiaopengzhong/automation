#@File   : .py
#@Time   : 2025/10/13 0:23
#@Author : 
#@Software: PyCharm
# tests/ui/test_mine_page.py
import pytest

from lib.flows.login_flow import LoginFlow
from lib.flows.mine_flow import MineFlow
from lib.utils.logger import setup_logging

logger = setup_logging("ui")

@pytest.mark.ui
@pytest.mark.mine
class TestMinePage:

    def test_my_page_orders_entry(self, driver):
        """验证‘我的’页面可进入订单列表页"""
        # 登录后进入首页
        login_flow = LoginFlow(driver)
        login_flow.login("user001", "123456")

        # 进入‘我的’页面
        driver.get("http://localhost:8060/#/pages/mine/index")
        mine_flow = MineFlow(driver)

        # 校验加载完成
        username = mine_flow.check_login_user()
        logger.info(f"当前登录用户: {username}")
        assert username, "用户名为空"

        # 点击“全部订单”，进入订单列表页
        order_page = mine_flow.open_my_orders()
        assert order_page.is_order_page_loaded(), "进入订单列表页失败"
