#@File   : .py
#@Time   : 2024/8/30 23:03
#@Author : 
#@Software: PyCharm
import json
import time
from functools import wraps
import allure
import pytest

from lib.apilib.crud import Crud
from lib.util.utlity import read_data

# 自定义装饰器，用于控制接口调用频率
def rate_limit(wait_time=2):  # 外层函数，接收一个参数 wait_time，用于指定等待时间（默认为2秒）
    def decorator(func):  # 内层函数，接收一个函数作为参数，这个函数就是要被装饰的目标函数
        @wraps(func)  # 使用 functools.wraps 保持原函数的元数据，例如函数名和文档字符串
        def wrapper(*args, **kwargs):  # 包装函数，用于包裹目标函数
            result = func(*args, **kwargs)  # 执行目标函数，并获取其返回值
            time.sleep(wait_time)  # 在目标函数执行后等待指定的时间（wait_time 秒）
            return result  # 返回目标函数的执行结果
        return wrapper  # 返回包装后的函数
    return decorator  # 返回装饰器

@pytest.mark.api
@allure.feature("新增接口用例")
class TestCrud:
    @pytest.fixture(scope='function')
    def crud(self, init_admin, request):
        crud = Crud(init_admin)
        allure.attach(json.dumps({"crud": str(crud)}, indent=4), name="初始化Crud对象",
                      attachment_type=allure.attachment_type.JSON)
        try:
            yield crud
        finally:
            # 通过 request 对象获取 recordid
            recordid = getattr(request.session, 'recordid', None)
            if recordid:
                crud.delete(recordIds=[recordid])
                allure.attach(f"清理记录ID:{recordid}", name="清理操作", attachment_type=allure.attachment_type.JSON)

    @pytest.mark.parametrize('params', read_data(file_path='case_data/crud.yaml')['submit'])
    def test_submit(self, crud, params, request):
        fieldData = params['fieldData']
        fieldName = params['fieldName']
        expected = params['expected']
        # 动态设置用例标题
        allure.dynamic.title(f"提交数据并验证提交结果：字段 {fieldName}")
        with allure.step("获取新增的响应数据"):
            try:
                # 使用rate_limit装饰器来控制接口调用频率
                @rate_limit(wait_time=2)
                def submit_data():
                    return crud.submit(fieldData=fieldData)
                result = submit_data()
                allure.attach(json.dumps(result, indent=4, ensure_ascii=False), "新增结果", allure.attachment_type.JSON)

                recordid = result['data']
                request.session.recordid = recordid  # 设置 session 级的 recordid
                #time.sleep(2)
            except Exception as e:
                allure.attach(str(e), "新增异常", allure.attachment_type.TEXT)
                pytest.fail(f"提交失败:{str(e)}")

        with allure.step("获取记录的详情数据里的{fieldName}字段的信息"):
            try:
                query_reponse = crud.detail(recordId=recordid)['data']['record']['rowData'][fieldName]
                allure.attach(json.dumps(query_reponse, indent=4, ensure_ascii=False), "记录详情里的{fieldName}字段的信息", allure.attachment_type.JSON)
            except KeyError as e:
                allure.attach(str(e),"查询详情异常", allure.attachment_type.TEXT)
                pytest.fail(f"查询详情失败：{str(e)}")
        with allure.step("对比实际结果与预期结果是否一致"):
            allure.attach(json.dumps({"expectrd": expected, "actual":query_reponse}, indent=4), "验证结果", allure.attachment_type.JSON)
            try:

                assert query_reponse == expected, f"预期值：{expected}，实际值：{query_reponse}"
            except AssertionError as e:
                allure.attach(json.dumps(query_reponse, indent=4, ensure_ascii=False), "实际结果（断言失败）", allure.attachment_type.JSON)
                allure.attach(str(expected), "预期的结果", allure.attachment_type.JSON)
                allure.attach(str(query_reponse), "实际的查询结果", allure.attachment_type.JSON)
                raise


