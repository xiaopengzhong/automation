#@File   : .py
#@Time   : 2025/10/1 2:32
#@Author : 
#@Software: PyCharm
import requests
import pytest

from lib.utils.db_util import DBUtils


@pytest.mark.api

class TestProductAPI:

    @pytest.fixture(scope="function", autouse=True)
    def setup_and_teardown(self):
        """前置后置：数据库连接"""
        self.db = DBUtils("default")
        yield
        self.db.close()

    def test_create_product(self):
        url = "http://192.168.220.128:8080/product/create"
        payload = {
            "name": "自动化测试商品",
            "productSn": "AUTO123456",
            "price": 1999,
            "brandName": "TestBrand",
            "deleteStatus": 0,
            "publishStatus": 1,
            "stock": 100
        }
        headers = {"Content-Type": "application/json"}

        # 发送请求
        resp = requests.post(url, json=payload, headers=headers)

        # 接口返回断言
        assert resp.status_code == 200
        assert resp.json().get("code") == 200

        # 数据库断言
        sql = f"SELECT * FROM pms_product WHERE productSn = '{payload['productSn']}'"
        result = self.db.query_one(sql)

        assert result is not None, "数据库中未找到新增的商品"
        assert result["name"] == payload["name"]
        assert result["price"] == payload["price"]
        assert result["stock"] == payload["stock"]
