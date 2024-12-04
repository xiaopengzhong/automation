#@File   : .py
#@Time   : 2024/12/4 0:00
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.util.utlity import read_data

@pytest.mark.api
@allure.feature('视图筛选器功能')
class Test_ViewCode:
    @allure.story("文本字段筛选")
    @pytest.mark.parametrize('params', read_data(file_path='case_data/viewcode.yaml')['filter_view'])
    def test_list_text(self, params, add_data):
        use_code = params['use_code']
        viewCode = params['viewcode']
        expected = params['expected']
        allure.dynamic.title(use_code)
        get_crud, add_payloads = add_data
        allure.attach(str(add_payloads), "提交数据的参数", allure.attachment_type.JSON)

        with allure.step("获取视图列表结果"):
            result = get_crud.list(viewCode=viewCode)
            allure.attach("查询参数", f"viewCode: {viewCode}", allure.attachment_type.TEXT)
            allure.attach("查询结果", f"{result}", allure.attachment_type.JSON)

        with allure.step("验证结果"):
            actual_total = result['page']['total']
            allure.attach("预期结果", f"{expected}", allure.attachment_type.TEXT)
            allure.attach("实际结果", f"{actual_total}", allure.attachment_type.TEXT)

            assert actual_total == expected, f"Expected {expected}, but got {actual_total}. Query: viewCode={viewCode}"