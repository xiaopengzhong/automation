# @File   : .py
# @Time   : 2023/7/13 0:22
# @Author :
# @Software: PyCharm
import json

# 请求公式接口
from lib.api.baseAPI import BaseAPI


class Formula(BaseAPI):
    def __init__(self, token):
        self.token = token
        super().__init__(token)
    def get_formula(self, **kwargs):
        url = f"/api-engine-mid/getFormulaAllResult"
        payload = self.payload['data']
        payload.update(**kwargs)
        resp = super().post(endpoint=url, json=payload)
        return resp.json()



