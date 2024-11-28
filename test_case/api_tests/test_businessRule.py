# @File   : .py
# @Time   : 2023/11/21 12:14
# @Author :
# @Software: PyCharm
import logging
import json
import allure
import pytest
from lib.util.utlity import read_data, rate_limit

logger = logging.getLogger()

# 全局装饰器封装
def rate_limited_submit(wait_time=2):
    """简化 rate_limit 装饰器的重复使用"""
    def decorator(func):
        return rate_limit(wait_time=wait_time)(func)
    return decorator

# 业务规则测试类
@pytest.mark.api
@allure.feature("业务规则")
class Test_BusinessRule:

    # fixture 用于初始化和清理工作
    @pytest.fixture()
    def manage_business_rule(self, get_crud, get_businessRule, request):
        """
        Fixture: 管理业务规则的启用和禁用
        """

        def enable_rule(rule_id):
            """启用业务规则"""
            logger.info(f"启用业务规则，ID: {rule_id}")

            @rate_limited_submit(wait_time=2)
            def businessRule_data():
                return get_businessRule.manage_businessRule(rule_id, isEnable=1)
            enable_result = businessRule_data()
            allure.attach(json.dumps({"crud": str(enable_result)}, indent=4), name="启用业务规则",
                          attachment_type=allure.attachment_type.JSON)
            return enable_result

        def disable_rule(rule_id, result=None):
            """禁用业务规则并清理数据"""
            logger.info(f"禁用业务规则，ID: {rule_id}")

            @rate_limited_submit(wait_time=2)
            def businessRule_data():
                return get_businessRule.manage_businessRule(rule_id, isEnable=0)
            disable_result = businessRule_data()
            allure.attach(json.dumps({"crud": str(disable_result)}, indent=4), name="禁用业务规则",
                          attachment_type=allure.attachment_type.JSON)
            if result and result.get('code') == 0:
                logger.info(f"删除数据，ID: {result['data']}")
                get_crud.delete(recordIds=[result['data']])

        yield enable_rule, disable_rule

        # 获取当前参数数据
        rule_id = getattr(request.node, 'rule_id', None)

        # 在测试结束后调用禁用规则和清理逻辑
        disable_rule(rule_id, getattr(request.node, 'result', None))

    # 参数化测试
    @pytest.mark.trylast
    @allure.story("启用业务规则-新增时触发业务规则")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/businessRule.yaml')['businessRule'])
    def test_text_businessRule(self, params, manage_business_rule, get_crud, request):
        """
        测试文本字段业务规则 - 启用业务规则
        """
        rule_id = params['id']  # 获取测试数据中的 id
        field_data = params['fieldData']
        expected = params['expected']

        allure.dynamic.title(f"{expected}")  # 使用动态标题

        enable_rule, disable_rule = manage_business_rule

        # 启用业务规则
        with allure.step("启用业务规则"):
            enable_rule(rule_id)

        # 记录 rule_id
        request.node.rule_id = rule_id

        # 提交数据并检查返回结果
        logger.info(f"开始提交数据，值: {field_data}")

        @rate_limited_submit(wait_time=2)
        def submit_data():
            return get_crud.submit(fieldData=field_data)

        with allure.step("新增数据时触发业务规则"):
            result = submit_data()

        # 记录结果
        request.node.result = result
        logger.info(f"提交结果：{result}")
        allure.attach("查询结果", f"{result}")

        # 断言新增数据时触发业务规则
        with allure.step("断言新增数据时触发业务规则"):
            assert result['msg'] == expected, f"预期结果: {expected}, 实际结果: {result['msg']}"

        # 禁用业务规则并清理
        with allure.step("禁用业务规则并清理数据"):
            disable_rule(rule_id, result)

        # 记录测试通过
        logger.info("测试用例执行成功")

    @pytest.mark.trylast
    @allure.story("禁用业务规则 - 新增时不触发业务规则")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/businessRule.yaml')['businessRule'])
    def test_text_businessRule_disabled(self, params, manage_business_rule, get_crud, request):
        """
        测试文本字段业务规则 - 禁用业务规则时正常新增
        """
        rule_id = params['id']  # 获取测试数据中的 id
        field_data = params['fieldData']
        expected = params['expected']

        allure.dynamic.title(f"{expected} (禁用业务规则)")  # 使用动态标题

        enable_rule, disable_rule = manage_business_rule

        # 禁用业务规则
        with allure.step("禁用业务规则"):
            disable_rule(rule_id)

        # 记录 rule_id
        request.node.rule_id = rule_id

        # 提交数据并检查返回结果
        logger.info(f"开始提交数据，值: {field_data}")

        @rate_limited_submit(wait_time=2)
        def submit_data():
            return get_crud.submit(fieldData=field_data)

        with allure.step("新增数据时不触发业务规则"):
            result = submit_data()

        # 记录结果
        request.node.result = result
        logger.info(f"提交结果：{result}")
        allure.attach("查询结果", f"{result}")

        # 断言新增数据时没有触发业务规则
        with allure.step("断言新增数据时未触发业务规则"):
            assert result['msg'] == 'ok', f"预期结果: 'ok', 实际结果: {result['msg']}"

        # 禁用业务规则并清理
        with allure.step("禁用业务规则并清理数据"):
            disable_rule(rule_id, result)

        # 记录测试通过
        logger.info("测试用例执行成功")
