#@File   : .py
#@Time   : 2025/10/17 23:41
#@Author : 
#@Software: PyCharm

# lib/api/order_api.py
import copy
from lib.api.user.baseAPI import BaseAPI
from lib.api.user.cart import CartAPI
from lib.api.user.login import LoginAPI


class OrderAPI(BaseAPI):
    """订单相关接口"""
    def __init__(self, token, payload_file=None):
        super().__init__(auth_token=token, payload_file=payload_file)
        # 共享 token 和 payload_file，初始化 CartAPI
        self.cart_api = CartAPI(token, payload_file=payload_file)

    def get_order_detail(self, order_id):
        """获取订单详情"""
        url = f"/order/detail/{order_id}"

        resp = self.get(endpoint=url, json=self.payload)

        return resp.json()


    def create_order(self, cart_items=None, **kwargs):
        """创建订单：可选择是否自动添加购物车"""
        url = "/order/generateOrder"
        payload = copy.deepcopy(self.payload.get("create", {}))
        payload.update({"cartIds": cart_items, **kwargs})
        resp = self.post(endpoint=url, json=payload)
        return resp.json()


    def generate_confirm_Order(self, cart_ids=None, **kwargs):
        """订单信息接口"""
        url = "/order/generateConfirmOrder"
        payload = copy.deepcopy(self.payload.get("generateConfirm", []))

        if cart_ids:
            payload = cart_ids

        resp = self.post(endpoint=url, json=payload)
        return resp.json()

    def list_order(self):
        """商品列表"""
        url = "/order/list?status=-1&pageNum=1&pageSize=5"

        resp = self.get(endpoint=url)  # 请求时不显式传入 headers
        return resp.json()
    def cancel_order(self, **kwargs):
        """取消订单"""
        url = "/order/cancelUserOrder"
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        payload = copy.deepcopy(self.payload.get("cancel_order", {}))
        payload.update(kwargs)
        resp = self.post(endpoint=url, data=payload, headers=headers)  # 请求时不显式传入 headers
        return resp.json()
    def delete_order(self, **kwargs):
        """取消订单"""
        url = "/order/deleteOrder"
        headers = {"Content-Type": "application/x-www-form-urlencoded;charset=UTF-8"}
        payload = copy.deepcopy(self.payload.get("cancel_order", {}))
        payload.update(kwargs)
        resp = self.post(endpoint=url, data=payload, headers=headers)
        return resp.json()



if __name__ == "__main__":
    # 示例代码
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get('auth_token')

    if not token:
        print("登录失败，无法获取 token")
    else:
        cart = CartAPI(token, payload_file="../../../case_data/api/user/payload.yaml")
        cart.add_cart()
        cartIds = [item["id"] for item in cart.list_cart()["data"]]
        order_api = OrderAPI(token, payload_file="../../../case_data/api/user/payload.yaml")
        # 创建订单
        create_result = order_api.create_order(cartIds=cartIds)  # 不传 cart_items，自动从购物车获取
        print("创建订单结果:", create_result)
        # 获取订单id
        order_id = create_result.get("data", {}).get("order", {}).get("id")
        # 获取订单详情
        order_detail = order_api.get_order_detail(order_id)
        print("获取订单详情:", order_detail)

        # 生成确认订单
        confirm_result = order_api.generate_confirm_Order(cart_ids=cartIds)
        print("订单确认信息:", confirm_result)
        # 获取订单列表
        result2 = order_api.list_order()
        print("订单列表:", result2)
        # 取消订单
        result3 = order_api.cancel_order(orderId=order_id)
        print("取消订单:", result3)