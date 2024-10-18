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

# 获取 logger 实例
logger = logging.getLogger()


@pytest.mark.api
@allure.feature("基础增删改查接口用例")
class TestCrud:
    @pytest.fixture()
    def get_crud(self, init_admin):
        """Fixture: 初始化并返回 Crud 对象"""
        crud = Crud(init_admin)
        logger.info("初始化 Crud 对象")
        # 使用 allure 附件记录初始化的 Crud 对象
        allure.attach(json.dumps({"crud": str(crud)}, indent=4), name="初始化Crud对象",
                      attachment_type=allure.attachment_type.JSON)
        return crud

    @pytest.fixture(scope='function')
    def cleanup_data(self, get_crud, request):
        """Fixture: 后置操作，自动清理创建的数据"""
        yield get_crud
        recordid = getattr(request.node, 'recordid', None)
        # 检查是否有记录 ID 需要删除
        if recordid:
            logger.info(f"清理数据，删除记录ID: {recordid}")
            get_crud.delete(recordIds=[recordid])
            allure.attach(f"清理记录ID: {recordid}", name="清理操作", attachment_type=allure.attachment_type.JSON)

    @pytest.fixture(scope='function')
    def create_and_cleanup_data(self, get_crud, request):
        """Fixture: 前置动作创建数据，后置动作清理数据"""
        logger.info("开始新增数据")

        @rate_limit(wait_time=2)  # 添加速率限制
        def submit_data():
            return get_crud.submit()

        try:
            response = submit_data()
            recordid = response['data']
            logger.info(f"新增数据成功，记录ID: {recordid}")
            allure.attach(f"新增记录ID: {recordid}", name="新增操作", attachment_type=allure.attachment_type.JSON)
            # 将 recordid 传递给 request 对象，供后续使用
            request.node.recordid = recordid
            yield recordid, get_crud
        except Exception as e:
            logger.error(f"新增数据失败: {str(e)}")
            allure.attach(str(e), "新增数据失败", allure.attachment_type.TEXT)
            pytest.skip(f"新增数据失败，跳过编辑接口测试: {str(e)}")
        finally:
            if recordid:
                logger.info(f"清理数据，删除记录ID: {recordid}")
                get_crud.delete(recordIds=[recordid])
                allure.attach(f"清理记录ID: {recordid}", name="清理操作", attachment_type=allure.attachment_type.JSON)

    def assert_field(self, get_crud, recordid, fieldName, expected):
        """封装的公共断言方法，验证某个字段的值是否与预期一致"""
        with allure.step(f"获取记录 {recordid} 中字段 {fieldName} 的值"):
            logger.info(f"获取记录ID为 {recordid} 的 {fieldName} 字段信息")
            # 获取记录详情数据
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

        # 对比实际结果与预期结果
        with allure.step("对比实际结果与预期结果"):
            logger.info(f"对比 {fieldName} 字段的实际结果与预期结果，预期值：{expected}，实际值：{query_response}")
            assert query_response == expected, f"预期值：{expected}，实际值：{query_response}"

    @allure.story("新增接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['submit'])
    def test_submit(self, params, cleanup_data, request):
        """测试新增接口的用例"""
        fieldData = params['fieldData']
        fieldName = params['fieldName']
        expected = params['expected']
        allure.dynamic.title(f"提交数据并验证提交结果：字段 {fieldName}")
        get_crud = cleanup_data
        logger.info(f"开始执行新增接口测试用例，字段: {fieldName}")

        with allure.step("提交数据"):
            try:
                @rate_limit(wait_time=2)
                def submit_data():
                    return get_crud.submit(fieldData=fieldData)

                result = submit_data()
                recordid = result['data']
                # 保存 recordid 以便后续清理
                request.node.recordid = recordid
                logger.info(f"数据提交成功，记录ID: {recordid}")
                allure.attach(json.dumps(result, indent=4, ensure_ascii=False), "新增结果", allure.attachment_type.JSON)
            except Exception as e:
                logger.error(f"提交失败: {str(e)}")
                allure.attach(str(e), "提交失败", allure.attachment_type.TEXT)
                pytest.fail(f"提交失败: {str(e)}")

        # 使用公共的断言方法验证结果
        self.assert_field(get_crud, recordid, fieldName, expected)
        logger.info(f"新增接口测试用例执行成功，字段: {fieldName}")

    @allure.story("编辑接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['submit'])
    def test_edit(self, create_and_cleanup_data, params):
        """测试编辑接口的用例"""
        fieldData = params['fieldData']
        fieldName = params['fieldName']
        expected = params['expected']
        allure.dynamic.title(f"更新 {fieldName} 字段")

        # 获取新增的记录ID
        with allure.step("获取新增的记录ID"):
            recordid, get_crud = create_and_cleanup_data
            logger.info(f"获取到新增的记录ID: {recordid}")
            allure.attach(str(recordid), "新增结果的记录ID", allure.attachment_type.JSON)

        # 更新字段值
        with allure.step(f"更新 {fieldName} 字段的值"):
            try:
                logger.info(f"开始编辑，记录ID: {recordid}，字段: {fieldName}")
                update_result = get_crud.edit(recordid, fieldData=fieldData)
                logger.info("更新数据成功")
                allure.attach(json.dumps(update_result, indent=4), "更新结果", allure.attachment_type.JSON)
            except Exception as e:
                logger.error(f"编辑失败: {str(e)}")
                allure.attach(str(e), "编辑失败", allure.attachment_type.TEXT)
                pytest.fail(f"编辑失败: {str(e)}")

        # 验证更新后的结果
        self.assert_field(get_crud, recordid, fieldName, expected)
        logger.info(f"编辑接口测试用例执行成功")

    @allure.story("详情接口测试用例")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['detail'])
    def test_detail(self, create_and_cleanup_data, params):
        """测试详情接口的用例"""
        fieldName = params['fieldName']
        expected = params['expected']
        titleName = params['titleName']
        allure.dynamic.title(titleName)

        # 获取新增的记录ID
        with allure.step("获取新增的记录ID"):
            recordid, get_crud = create_and_cleanup_data
            logger.info(f"获取到新增的记录ID: {recordid}")
            allure.attach(str(recordid), "新增结果的记录ID", allure.attachment_type.JSON)

        if fieldName == '测试不存在的记录':
            # 使用错误的 recordid 进行查询，测试不存在的数据
            wrong_recordid = 100
            query_response = get_crud.detail(recordId=wrong_recordid).get('msg', None)
            assert query_response == expected, f"预期值：{expected}，实际值：{query_response}"
        else:
            # 验证正常记录的详情字段值
            self.assert_field(get_crud, recordid, fieldName, expected)

    @pytest.fixture(scope='function')
    def add_data(self, get_crud):
        """Fixture: 新增多条数据，后置操作清理数据"""
        created_records = []
        add_payloads = read_data(file_path='case_data/add_data.yaml')['fieldData']

        @rate_limit(wait_time=2)
        def submit_data(payload):
            response = get_crud.submit(fieldData=payload)
            return response['data']

        for payload in add_payloads:
            record_id = submit_data(payload)
            created_records.append(record_id)
            logger.info(f"Created record ID: {record_id}")

        allure.attach(str(created_records), "新增记录的ID", allure.attachment_type.JSON)
        yield get_crud, add_payloads

        # 清理已创建的记录
        get_crud.delete(recordIds=created_records)
        allure.attach(str(created_records), "删除的记录ID", allure.attachment_type.JSON)
        logger.info("清理完毕，已删除记录")

    @allure.story("列表接口测试用例")
    def test_list(self, add_data):
        """测试列表接口的用例"""
        allure.dynamic.title("测试列表里各个字段是否返回正确")

        with allure.step("调用 fixture 创建数据并返回创建的参数"):
            get_crud, add_payloads = add_data
            allure.attach(str(add_payloads), "提交数据的参数", allure.attachment_type.JSON)

        row_data = []
        page = 1
        # 分页获取数据，直到获取完所有页面
        while True:
            with allure.step("获取列表记录"):
                response = get_crud.list(page=page)
                page_data = response.get("data", [])
                row_data.extend(page_data)
                logger.info(f"获取的列表记录: {response}")
                allure.attach(str(response), "获取的列表记录", allure.attachment_type.JSON)
                if len(page_data) < 20:
                    break  # 如果当前页面的数据少于20条，停止分页
                page += 1
        logger.info(f"row_data的值: {row_data}")

        # Helper function to validate each field
        def validate_fields(actual, expected):
            for key, value in expected.items():
                actual_value = actual.get(key)
                assert actual_value == value, f"字段 '{key}' 值不正确，期望: {value}，实际: {actual_value}"

        # 验证每条记录的字段
        for idx, expected_record in enumerate(add_payloads):
            created_record = row_data[-(idx + 1)].get("rowData", {})
            with allure.step(f"对比第 {idx + 1} 条记录的实际结果与预期结果是否一致"):
                validate_fields(created_record, expected_record)
