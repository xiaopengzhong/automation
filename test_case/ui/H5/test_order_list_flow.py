#@File   : .py
#@Time   : 2025/10/5 17:34
#@Author : 
#@Software: PyCharm
# tests/ui/test_order_list.py
import allure
import pytest
import time

from lib.flows.order_flow_list import OrderFlow
from lib.utils.logger import setup_logging

logger = setup_logging("ui")
@pytest.mark.ui
@allure.feature("订单列表模块")
class TestOrderList:

    def test_order_list_display(self, driver):
        """验证订单列表展示正常"""
        order_flow = OrderFlow(driver)
        order_page = order_flow.create_and_pay_order("user001", "123456", "iPhone")

        assert order_page.is_order_page_loaded(), "订单列表页未加载成功"
        order_info = order_page.get_first_order_info()
        logger.info(f"最新订单信息: {order_info}")

        # === 实际企业常用断言点 ===
        assert order_info["name"], "❌ 商品名称为空"
        assert "￥" in order_info["amount"], "❌ 订单金额格式错误"
        assert order_info["status"] in ["等待发货", "待收货", "已完成", "交易关闭"], f"❌ 状态异常: {order_info['status']}"
        assert order_info["order_time"], "❌ 订单时间为空"

    def test_switch_order_tabs(self, driver):
        """验证订单状态切换功能"""
        order_flow = OrderFlow(driver)
        order_page = order_flow.create_and_pay_order("user001", "123456", "iPhone")

        for tab in ["待付款", "待收货", "已完成"]:
            order_page.switch_tab(tab)
            time.sleep(1)
            assert order_page.is_order_page_loaded(), f"切换到 {tab} 失败"
            logger.info(f"✅ 成功切换到标签页：{tab}")