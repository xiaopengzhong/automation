# @File   : .py
# @Time   : 2023/7/14 0:31
# @Author :
# @Software: PyCharm
import json
import allure
import pytest

from lib.util.config_loader import read_data


@pytest.mark.api
@allure.feature('公式-系统变量功能和全部对象字段')
class Test_Formula:
    @pytest.mark.parametrize('params', read_data(file_path='case_data/formula.yaml')['formula'])
    def test_formula_01(self, before_formula, params):
        """
        系统变量用例
        :param before_formula: 前置条件的公式对象
        :param expressions: 表达式列表
        :param expression_name: 表达式名称
        :param expected: 预期结果
        :return: None
        """
        formula = before_formula
        expression_name = params['expression_name']
        expressions = params['expressions']
        expected = params['expected']
        allure.dynamic.title(f" {expression_name}公式结果验证")
        with allure.step("初始化测试环境"):
            env_info = {"host": formula.base_url, "API Version": "v2"}
            allure.attach(json.dumps(env_info, indent=4), "测试环境信息", allure.attachment_type.JSON)
        with allure.step("获取公式结果"):
            try:
                result = formula.get_formula(expressions=expressions)
                allure.attach(json.dumps(result, indent=4, ensure_ascii=False), "公式结果", allure.attachment_type.JSON)
            except Exception as e:
                allure.attach(str(e), "获取公式结果异常", allure.attachment_type.TEXT)
                raise
        with allure.step("验证公式结果是否与预期值一致"):
            actual_result = result.get('data', {}).get('data', [None])[0]
            allure.attach(json.dumps({"expected": expected, "actual": actual_result}, indent=4),
                          "验证结果", allure.attachment_type.JSON)
            try:
                assert actual_result == expected, f"预期值: {expected}, 实际值: {actual_result}"
            except AssertionError as e:
                allure.attach(json.dumps(result, indent=4, ensure_ascii=False), "实际结果（断言失败）", allure.attachment_type.JSON)
                allure.attach(str(expected), "预期结果", allure.attachment_type.TEXT)
                allure.attach(str(actual_result), "实际结果", allure.attachment_type.TEXT)
                raise

