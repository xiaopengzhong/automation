#@File   : .py
#@Time   : 2025/10/1 2:29
#@Author : 
#@Software: PyCharm
import requests

from lib.api.admin.baseAPI import BaseAPI


class ProductAPI(BaseAPI):
    def __init__(self, token):
        self.token = token
        super().__init__()

    def create_product(self, **kwargs):
        url = "/product/create"
        payload = self.payload['data']
        payload.update(**kwargs)
        resp = super().post(endpoint=url, json=payload)
        return resp
