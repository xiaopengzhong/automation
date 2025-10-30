#@File   : .py
#@Time   : 2025/10/3 14:31
#@Author : 
#@Software: PyCharm
# lib/api/user/cart.py
import copy
from lib.api.user.baseAPI import BaseAPI
from lib.api.user.login import LoginAPI
class CartAPI(BaseAPI):
    def __init__(self, token, payload_file=None):
        super().__init__(auth_token=token, payload_file=payload_file)

    def clear_cart(self):
        """清空购物车"""
        url = "/cart/clear"
        payload = self.payload
        resp = self.post(endpoint=url, json=payload)
        return resp.json()

    def add_cart(self, **kwargs):
        """添加商品到购物车"""
        url = "/cart/add"
        payload = copy.deepcopy(self.payload.get("add_cart", {}))
        payload.update(kwargs)
        resp = self.post(endpoint=url, json=payload)  # 请求时不显式传入 headers
        return resp.json()
    def list_cart(self):
        """添加商品到购物车"""
        url = "/cart/list"
        resp = self.get(endpoint=url)  # 请求时不显式传入 headers
        return resp.json()
    def update_quantity_cart(self,id,quantity):
        """添加商品到购物车"""
        url = f"/cart/update/quantity?id={id}&quantity={quantity}"

        resp = self.get(endpoint=url)  # 请求时不显式传入 headers

        return resp.json()
    def delete_cart(self,ids):
        """添加商品到购物车"""
        url = f"/cart/delete?ids={ids}"
        payload = self.payload

        resp = self.post(endpoint=url, json=payload)  # 请求时不显式传入 headers
        return resp.json()

    def ensure_cart_has_item(self):
        """确保购物车中至少有一个商品"""
        result = self.list_cart()
        items = result.get("data", [])
        if not items:
            self.add_cart()
            result = self.list_cart()
            items = result.get("data", [])
        return items[0]["id"]


if __name__ == "__main__":
    # 登录获取 token
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get('auth_token')
    print(f"获取到的 token: {token}")
    # 添加商品到购物车

    # 清空购物车
    cart_api = CartAPI(token, payload_file="../../../case_data/api/user/payload.yaml")




    result2 = cart_api.add_cart()  # 加入购物车
    print("添加商品到购物车结果:", result2)

    result3 = cart_api.list_cart()  # 购物车列表
    cart_id = result3['data'][0]['id']
    print("购物车列表:", result3)

    result4 = cart_api.update_quantity_cart(cart_id, 4)  # 示例参数
    print("修改商品数量:", result4)

    result5 = cart_api.delete_cart(cart_id)  # 示例参数
    print("购物车删除商品:", result5)

    result = cart_api.clear_cart()
    print("清空购物车结果:", result)

    result7 = cart_api.ensure_cart_has_item()
    print("确保购物车有商品:", result7)
