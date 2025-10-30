#@File   : .py
#@Time   : 2025/10/18 14:05
#@Author : 
#@Software: PyCharm
#lib/api/user/product.py

from lib.api.user.baseAPI import BaseAPI
from lib.api.user.login import LoginAPI
class ProductAPI(BaseAPI):
    """商品相关接口"""

    def __init__(self, token, payload_file=None):
        super().__init__(auth_token=token, payload_file=payload_file)

    def search_pruduct(self, keyword):
        """添加商品到购物车"""
        url = f"/product/search?keyword={keyword}&pageNum=1&pageSize=10"
        resp = self.get(endpoint=url)  # 请求时不显式传入 headers
        return resp.json()

    def detail_pruduct(self, productId):
        """添加商品到购物车"""
        url = f"/product/detail/{productId}"

        resp = self.get(endpoint=url)  # 请求时不显式传入 headers
        return resp.json()

    def cate_list_pruduct(self, number):
        """添加商品到购物车,number:0、1、2、3、4、5、52"""
        url = f"/home/productCateList/{number}"
        resp = self.get(endpoint=url)  # 请求时不显式传入 headers
        return resp.json()



if __name__ == "__main__":
    # 登录获取 token
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get('auth_token')
    print(f"获取到的 token: {token}")

    # 商品搜索
    product_api = ProductAPI(token, payload_file="../../../case_data/api/user/payload.yaml")
    result = product_api.search_pruduct("iphone")
    print("搜索商品结果:", result)
    product_id = result.get("data", {}).get("list", [])[0]['id']  # 获取搜索结果的第一个id


    # 获取商品详情
    result1 = product_api.detail_pruduct(product_id)
    print("商品详情结果:", result1)
    # 商品分类
    result2 = product_api.cate_list_pruduct(1)
    print("获取商品分类:", result2)