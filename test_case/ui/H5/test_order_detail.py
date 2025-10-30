#@File   : .py
#@Time   : 2025/10/12 16:22
#@Author : 
#@Software: PyCharm
# tests/ui/test_order_detail.py
import allure
import pytest

from lib.api.user.order import OrderApi
from lib.flows.order_detail_flow import OrderDetailFlow


# tests/ui/test_order_detail.py
import pytest


from lib.flows.order_flow_list import OrderFlow
from lib.utils.logger import setup_logging

logger = setup_logging("ui")

@pytest.mark.ui
class TestOrderDetail:

    def test_order_detail_info(self, driver, order_id):
        """验证订单详情信息展示正确"""

        # 1️⃣ 获取接口数据
        api_data = OrderApi().get_order_detail(order_id)


        # 2️⃣ UI进入详情页
        order_detail_flow = OrderDetailFlow(driver)
        detail_page = order_detail_flow.open_first_order_detail()

        ui_data = detail_page.get_order_detail_info()

        # 3️⃣ 断言前处理：格式化金额
        api_expected = {
            "order_no": api_data["orderSn"],
            "status": api_data["statusDesc"],
            "receiver_name": api_data["receiverName"],
            "receiver_phone": api_data["receiverPhone"],
            "receiver_address": api_data["receiverAddress"],
            "product_name": api_data["productList"][0]["productName"],
            "product_price": f"¥{api_data['productList'][0]['productPrice']:.2f}",
            "product_quantity": str(api_data["productList"][0]["productQuantity"]),
            "actual_amount_paid": f"¥{api_data['payAmount']:.2f}"
        }
        # 4️⃣ 执行断言
        for key, expected_value in api_expected.items():
            with allure.step(f"验证字段：{key}"):
                ui_value = ui_data.get(key)
                logger.info(f"[断言] {key}: 页面={ui_value}, 接口={expected_value}")
                assert ui_value == expected_value, f"{key} 不一致！UI: {ui_value}, API: {expected_value}"