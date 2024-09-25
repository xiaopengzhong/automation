#@File   : .py
#@Time   : 2024/8/30 23:03
#@Author : 
#@Software: PyCharm
import json
import logging
import allure
import pytest
from lib.apilib.crud import Crud
from lib.util.utlity import read_data, rate_limit, record_execution_time

logger = logging.getLogger()


@pytest.mark.api
@allure.feature("基础增删改查接口用例")
class TestCrud:
    @pytest.fixture()
    def get_crud(self, init_admin):
        """返回Crud对象"""
        crud = Crud(init_admin)
        logger.info("初始化 Crud 对象")
        allure.attach(json.dumps({"crud": str(crud)}, indent=4), name="初始化Crud对象",
                      attachment_type=allure.attachment_type.JSON)
        return crud

    @pytest.fixture(scope='function')
    def cleanup_data(self, get_crud, request):
        """后置删除数据"""
        yield get_crud
        recordid = getattr(request.node, 'recordid', None)
        if recordid:
            logger.info(f"fixture后置动作，开始清理数据，删除记录ID: {recordid}")
            get_crud.delete(recordIds=[recordid])
            allure.attach(f"清理记录ID: {recordid}", name="清理操作", attachment_type=allure.attachment_type.JSON)

    @pytest.fixture(scope='function')
    def create_and_cleanup_data(self, get_crud, request):
        logger.info("fixture前置动作，开始新增数据")

        @rate_limit(wait_time=2)
        def submit_data():
            return get_crud.submit()

        try:
            response = submit_data()
            recordid = response['data']
            logger.info(f"新增数据成功，记录ID: {recordid}")
            allure.attach(f"新增记录ID: {recordid}", name="新增操作", attachment_type=allure.attachment_type.JSON)
            request.node.recordid = recordid  # 保存到 request.node
            yield recordid, get_crud
        except Exception as e:
            logger.error(f"新增数据失败: {str(e)}")
            allure.attach(str(e), "新增数据失败", allure.attachment_type.TEXT)
            pytest.skip(f"新增数据失败，跳过编辑接口测试: {str(e)}")
        finally:
            if recordid:
                logger.info(f"fixture后置动作，开始清理数据，删除记录ID: {recordid}")
                get_crud.delete(recordIds=[recordid])
                allure.attach(f"清理记录ID: {recordid}", name="清理操作", attachment_type=allure.attachment_type.JSON)

    def assert_field(self, get_crud, recordid, fieldName, expected):
        """封装的公共断言方法，用于对比实际结果与预期结果"""
        with allure.step(f"获取记录的详情数据里的 {fieldName} 字段的信息"):
            logger.info(f"开始获取记录ID为 {recordid} 的 {fieldName} 字段的信息")
            query_response = (
                get_crud.detail(recordId=recordid)
                    .get('data', {})
                    .get('record', {})
                    .get('rowData', {})
                    .get(fieldName, None)
            )
            logger.info(f"{fieldName} 字段的值为：{query_response}")
            allure.attach(json.dumps(query_response, indent=4, ensure_ascii=False), f"{fieldName}字段的信息",
                          allure.attachment_type.JSON)

        with allure.step("对比实际结果与预期结果是否一致"):
            logger.info(f"开始对比 {fieldName} 字段的实际结果与预期结果，预期值：{expected}，实际值：{query_response}")
            assert query_response == expected, f"预期值：{expected}，实际值：{query_response}"

    @allure.story("新增接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['submit'])
    def test_submit(self, params, cleanup_data, request):
        """新增接口测试用例"""
        fieldData = params['fieldData']
        fieldName = params['fieldName']
        expected = params['expected']
        allure.dynamic.title(f"提交数据并验证提交结果：字段 {fieldName}")
        get_crud = cleanup_data
        logger.info(f"开始执行新增接口测试用例，测试新增字段: {fieldName}")
        with allure.step("提交数据"):
            try:
                @rate_limit(wait_time=2)
                def submit_data():
                    return get_crud.submit(fieldData=fieldData)
                result = submit_data()
                recordid = result['data']
                request.node.recordid = recordid  # 保存 recordid
                logger.info(f"数据提交成功，记录ID: {recordid}")
                allure.attach(json.dumps(result, indent=4, ensure_ascii=False), "新增结果", allure.attachment_type.JSON)
            except Exception as e:
                logger.error(f"提交失败: {str(e)}")
                allure.attach(str(e), "提交失败", allure.attachment_type.TEXT)
                pytest.fail(f"提交失败: {str(e)}")

        # 使用公共的断言方法
        self.assert_field(get_crud, recordid, fieldName, expected)
        logger.info(f"新增接口测试用例执行成功，字段: {fieldName}")
    @allure.story("编辑接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['submit'])
    def test_edit(self, create_and_cleanup_data, params):
        """编辑接口测试用例"""
        fieldData = params['fieldData']
        fieldName = params['fieldName']
        expected = params['expected']
        allure.dynamic.title(f"更新 {fieldName} 字段")
        # 获取新增的记录ID
        with allure.step("获取到新增的记录ID"):
            recordid, get_crud = create_and_cleanup_data
            logger.info(f"获取到新增的记录ID: {recordid}")
            allure.attach(str(recordid), "新增结果的记录ID", allure.attachment_type.JSON)
        # 更新字段
        with allure.step(f"更新 {fieldName} 字段的值"):
            try:
                logger.info(f"开始执行编辑接口测试用例，编辑的记录ID: {recordid}，编辑的字段: {fieldName}")
                update_result = get_crud.edit(recordid, fieldData=fieldData)
                logger.info(f"更新数据成功")
                allure.attach(json.dumps(update_result, indent=4), "更新结果", allure.attachment_type.JSON)
            except Exception as e:
                logger.error(f"编辑失败: {str(e)}")
                allure.attach(str(e), "编辑失败", allure.attachment_type.TEXT)
                pytest.fail(f"编辑失败: {str(e)}")
        # 使用公共的断言方法
        self.assert_field(get_crud, recordid, fieldName, expected)
        logger.info(f"编辑接口测试用例执行成功")

    @allure.story("详情接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['detail'])
    def test_detail(self, create_and_cleanup_data, params):
        """详情接口测试用例"""
        fieldName = params['fieldName']
        expected = params['expected']
        titleName = params['titleName']
        allure.dynamic.title(titleName)
        with allure.step("获取到新增的记录ID"):
            # 获取新增的记录ID
            recordid, get_crud = create_and_cleanup_data
            logger.info(f"获取到新增的记录ID: {recordid}")
            allure.attach(str(recordid), "新增结果的记录ID", allure.attachment_type.JSON)
        if fieldName == '测试不存在的记录':
            # 使用错误的 recordid 进行查询
            wrong_recordid = 100
            query_response = get_crud.detail(recordId=wrong_recordid).get('msg', None)
            assert query_response == expected, f"预期值：{expected}，实际值：{query_response}"
        else:
            # 正常记录的验证
            self.assert_field(get_crud, recordid, fieldName, expected)

