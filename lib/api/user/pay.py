#@File   : .py
#@Time   : 2025/10/18 23:20
#@Author : 
#@Software: PyCharm
# lib/api/user/pay.py
import copy


from lib.api.user.baseAPI import BaseAPI
from lib.api.user.login import LoginAPI
from lib.api.user.order import OrderAPI  # 确保路径正确


class PayAPI(BaseAPI):
    """支付相关接口"""

    def __init__(self, token, payload_file=None):
        super().__init__(auth_token=token, payload_file=payload_file)
        # 初始化 OrderAPI，共享 token 和 payload
        self.order_api = OrderAPI(token, payload_file=payload_file)

    def success_pay(self, **kwargs):
        """模拟支付成功接口"""
        url = "/order/paySuccess"
        payload = copy.deepcopy(self.payload.get("paysuccess", {}))

        # 1. 创建订单
        self.logger.info("开始创建订单...")
        order_resp = self.order_api.create_order()
        if not order_resp or "error" in order_resp:
            error_msg = order_resp.get("error", "未知错误")
            self.logger.error(f"创建订单失败: {error_msg}")
            return {"error": "Order creation failed", "details": error_msg}

        # 2. 提取 orderId
        try:
            order_data = order_resp.get("data", {})
            if not order_data:
                self.logger.error("订单数据为空")
                return {"error": "No order data returned"}
            order_id = order_data.get("order").get("id")
            if not order_id:
                self.logger.error("无法获取 orderId")
                return {"error": "Missing orderId in response"}
            self.logger.info(f"获取到 orderId: {order_id}")
        except Exception as e:
            self.logger.error(f"解析订单ID失败: {e}")
            return {"error": "Failed to parse orderId", "details": str(e)}

        # 3. 更新支付 payload
        payload.update({"orderId": order_id, **kwargs})

        # 4. 发送支付成功请求
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}

        resp = self.post(endpoint=url, data=payload, headers=headers)

        return resp.json()

if __name__ == "__main__":
    # 登录获取 token
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get('auth_token')

    if not token:
        print("登录失败，无法获取 token")
    else:
        print(f"登录成功，token: {token}")
        pay_api = PayAPI(token, payload_file="../../../case_data/api/user/payload.yaml")
        result = pay_api.success_pay()
        print("支付成功结果:", result)