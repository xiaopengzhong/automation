# @File   : .py
# @Time   : 2023/11/21 12:14
# @Author :
# @Software: PyCharm
import logging
import json
import allure
import pytest
from lib.util.utlity import read_data, rate_limit, attach_log

logger = logging.getLogger()



# 业务规则测试类
@pytest.mark.api
@allure.feature("业务规则")
class TestBusinessRule:
    @pytest.fixture()
    def manage_business_rule(self, get_crud, get_businessRule, request):
        """
        Fixture: 管理业务规则的启用和禁用
        """

        @rate_limit(wait_time=2)
        def enable_rule(rule_id):
            logger.info(f"启用业务规则，ID: {rule_id}")
            result = get_businessRule.manage_businessRule(rule_id, isEnable=1)
            attach_log(result, "启用业务规则")
            return result

        @rate_limit(wait_time=2)
        def disable_rule(rule_id, recordIds=None):
            logger.info(f"禁用业务规则，ID: {rule_id}")
            result = get_businessRule.manage_businessRule(rule_id, isEnable=0)
            attach_log(result, "禁用业务规则")

            # 清理数据
            if recordIds:
                logger.info(f"删除数据，ID: {recordIds}")
                get_crud.delete(recordIds=recordIds)


        yield enable_rule, disable_rule

        # 清理：禁用业务规则和删除数据
        rule_id = getattr(request.node, 'rule_id', None)
        disable_rule(rule_id, getattr(request.node, 'recordIds', None))

    # 错误校验业务规则
    @pytest.mark.trylast
    @allure.story("启用业务规则-新增时触发业务规则")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/businessRule.yaml')['error_businessRule'])
    def test_error_businessRule_enable(self, params, manage_business_rule, get_crud, request):
        """
        测试文本字段业务规则 - 启用业务规则
        """
        rule_id = params['id']  # 获取测试数据中的 id
        field_data = params['fieldData']
        expected = params['expected']
        use_case = params['use_case']

        allure.dynamic.title(f"{use_case}")  # 使用动态标题

        enable_rule, disable_rule = manage_business_rule

        # 启用业务规则
        with allure.step("启用业务规则"):
            enable_rule(rule_id)

        # 记录 rule_id
        request.node.rule_id = rule_id

        # 提交数据并检查返回结果
        logger.info(f"开始提交数据，值: {field_data}")

        @rate_limit(wait_time=2)
        def submit_data():
            return get_crud.submit(fieldData=field_data)

        with allure.step("新增数据时触发业务规则"):
            result = submit_data()
            # 如果新增成功则需要把id传给fixtrue删除掉记录
            recordIds = []
            if result.get('code') == 0:
                recordId = result.get('data')
                recordIds.append(recordId)
                request.node.recordIds = recordIds



        logger.info(f"提交结果：{result}")
        allure.attach("查询结果", f"{result}")

        # 断言新增数据时触发业务规则
        with allure.step("断言新增数据时触发业务规则"):
            assert result['msg'] == expected, f"预期结果: {expected}, 实际结果: {result['msg']}"


        # 记录测试通过
        logger.info("测试用例执行成功")

    @pytest.mark.trylast
    @allure.story("禁用业务规则 - 新增时不触发业务规则")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/businessRule.yaml')['error_businessRule'])
    def test_error_businessRule_disabled(self, params, manage_business_rule, get_crud, request):
        """
        测试文本字段业务规则 - 禁用业务规则时正常新增
        """
        rule_id = params['id']  # 获取测试数据中的 id
        field_data = params['fieldData']
        use_case = params['use_case']

        allure.dynamic.title(f"{use_case} (禁用业务规则)")  # 使用动态标题

        enable_rule, disable_rule = manage_business_rule

        # 禁用业务规则
        with allure.step("禁用业务规则"):
            disable_rule(rule_id)

        # 记录 rule_id
        request.node.rule_id = rule_id

        # 提交数据并检查返回结果
        logger.info(f"开始提交数据，值: {field_data}")

        @rate_limit(wait_time=2)
        def submit_data():
            return get_crud.submit(fieldData=field_data)

        with allure.step("新增数据时不触发业务规则"):
            result = submit_data()
            # 如果新增成功则需要把id传给fixtrue删除掉记录
            recordIds = []
            if result.get('code') == 0:
                recordId = result.get('data')
                recordIds.append(recordId)
                request.node.recordIds = recordIds



        logger.info(f"提交结果：{result}")
        allure.attach("查询结果", f"{result}")

        # 断言新增数据时没有触发业务规则
        with allure.step("断言新增数据时未触发业务规则"):
            assert result['msg'] == 'ok', f"预期结果: 'ok', 实际结果: {result['msg']}"


        # 记录测试通过
        logger.info("测试用例执行成功")



    # 唯一校验业务规则
    @pytest.mark.trylast
    @allure.story("启用唯一校验业务规则-新增时触发业务规则")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/businessRule.yaml')['unique_businessRule'])
    def test_unique_business_rule(self, params, manage_business_rule, get_crud, request):
        """
        测试文本字段业务规则 - 启用业务规则
        """
        rule_id = params['id']
        field_data = params['fieldData']
        expected = params['expected']
        use_case = params['use_case']

        # 动态标题
        allure.dynamic.title(expected)
        logger.info(f"开始测试：{use_case}")

        enable_rule, disable_rule = manage_business_rule

        # 启用业务规则
        with allure.step("启用业务规则"):
            enable_rule(rule_id)
        request.node.rule_id = rule_id  # 记录 rule_id

        # 提交数据方法
        @rate_limit(wait_time=2)
        def submit_data(data):
            result = get_crud.submit(fieldData=data)
            logger.info(f"提交数据：{data}, 返回结果：{result}")
            return result

        # 第一次提交
        with allure.step("第一次新增数据时不触发业务规则"):
            result1 = submit_data(field_data)
            attach_log(result1, "第一次提交结果")

        # 第二次提交
        with allure.step("第二次新增数据时触发业务规则"):
            result2 = submit_data(field_data)
            attach_log(result2, "第二次提交结果")
        # 如果新增成功则需要把id传给fixtrue删除掉记录
        recordIds = []

        # 判断 result1 和 result2 的 code 是否为 0，并且只添加有效的 data
        if result1.get('code') == 0:
            recordIds.append(result1.get('data'))

        if result2.get('code') == 0:
            recordIds.append(result2.get('data'))

        # 如果 recordIds 不为空，才记录它
        if recordIds:
            request.node.recordIds = recordIds

        # 断言
        with allure.step("断言新增数据时触发业务规则"):
            assert result2['msg'] == expected, f"预期结果: {expected}, 实际结果: {result2['msg']}"
        logger.info("测试用例执行成功")