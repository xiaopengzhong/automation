#@File   : .py
#@Time   : 2025/10/19 16:56
#@Author : 
#@Software: PyCharm
import pytest
import allure
from lib.api.user.login import LoginAPI
from lib.api.user.product import ProductAPI
from lib.utils.config_loader import load_yaml

@pytest.fixture(scope="class")
def product_api():
    login_api = LoginAPI()
    login_result = login_api.login(username="user001", password="123456")
    token = login_result.get("auth_token")
    api = ProductAPI(token, payload_file="case_data/api/user/payload.yaml")
    return api
@pytest.mark.api
@allure.epic("商城接口自动化")
@allure.feature("商品模块")
class TestProductAPI:


    @allure.story("搜索商品")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/product.yaml")["search_product"])
    @allure.title("搜索关键字：{data[keyword]} → 预期结果：{data[expected][message]}")
    def test_search_product(self, data, product_api):
        keyword = data["keyword"]
        expected = data["expected"]

        resp = product_api.search_pruduct(keyword)

        # 状态断言
        assert resp["code"] == expected["code"]
        assert resp["message"] == expected["message"]

        # 结构断言
        assert expected["contain_key"] in resp["data"]

        # 提取商品列表
        product_list = resp["data"].get("list", [])

        # ✅ 场景 1：空字符串（返回所有商品）
        if keyword == "":
            assert len(product_list) > 0, "搜索空字符串应返回全部商品，但结果为空"
            first_product = product_list[0]
            for field in expected["contain_field"]:
                assert field in first_product, f"字段缺失：{field}"

        # ✅ 场景 2：正常关键字（应有结果并匹配关键字）
        elif expected["name_keyword"]:
            assert len(product_list) > 0, f"搜索 '{keyword}' 期望有结果，但列表为空"
            first_product = product_list[0]
            for field in expected["contain_field"]:
                assert field in first_product, f"字段缺失：{field}"
            assert expected["name_keyword"].lower() in first_product["name"].lower(), \
                f"商品名称不包含关键字：{expected['name_keyword']}"

        # ✅ 场景 3：无效关键字（应返回空列表）
        else:
            assert len(product_list) == 0, f"搜索 '{keyword}' 期望无结果，但返回了 {len(product_list)} 条"

    # ========================= 商品详情 =========================
    @allure.story("商品详情")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/product.yaml")["detail_product"])
    @allure.title("商品ID：{data[product_id]} → 预期结果：{data[expected][message]}")
    def test_detail_product(self, data, product_api):
        product_id = data["product_id"]
        expected = data["expected"]

        resp = product_api.detail_pruduct(product_id)
        assert resp["code"] == expected["code"]
        assert resp["message"] == expected["message"]

        # ✅ 如果商品存在，则校验字段
        if resp["code"] == 200:
            product_info = resp["data"]
            for field in expected["contain_field"]:
                assert field in product_info['product']
            assert product_info['product']["id"] == expected["id"]
        else:
            # ✅ 商品不存在的场景
            assert resp["message"] == expected["message"]

    # ========================= 分类商品列表 =========================
    @allure.story("商品分类列表")
    @pytest.mark.parametrize("data", load_yaml("case_data/api/user/product.yaml")["cate_list_product"])
    @allure.title("分类编号：{data[number]} → 预期结果：{data[expected][message]}")
    def test_cate_list_product(self, data, product_api):
        number = data["number"]
        expected = data["expected"]

        resp = product_api.cate_list_pruduct(number)
        assert resp["code"] == expected["code"]
        assert resp["message"] == expected["message"]

        cate_list = resp.get("data", [])

        # ✅ 场景 1：有分类
        if cate_list:
            first_cate = cate_list[0]
            for field in expected["contain_field"]:
                assert field in first_cate
            assert len(cate_list) > 0
        # ✅ 场景 2：空分类或异常
        else:
            assert isinstance(cate_list, list)
            assert len(cate_list) == 0
