# @File   : .py
# @Time   : 2023/11/21 11:27
# @Author :
# @Software: PyCharm
import json

import requests

from conf.env import paas_host


# 业务规则禁用启用
from lib.api.login import paas_get_auth_tokens


# 禁用和启用业务规则
from lib.util.config_loader import read_data


class BusinessRule:
    def __init__(self, token):
        self.token = token

    def manage_businessRule(self, _id, **kwargs):
        url = f'{paas_host}/api-meta/form/businessRule/disable/{_id}'
        payload = read_data()['BusinessRule']['list']
        headers = {
            "Content-Type": "application/json;charset=UTF-8",
            "Cookie": "_bl_uid=qdlFeiX0y1FdXe1wkg6I5sd6n8da",
            "X-Expend-Log-App-Id": "51496",
            "X-User-Token": self.token
        }
        payload.update(kwargs)
        data = json.dumps(payload)
        resp = requests.post(url=url, data=data, headers=headers)
        return resp.json()


if __name__ == '__main__':
    br = BusinessRule(paas_get_auth_tokens())
    print(br.manage_businessRule(1765, isEnable=0))
