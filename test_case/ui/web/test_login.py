#@File   : .py
#@Time   : 2024/9/3 22:50
#@Author : 
#@Software: PyCharm

import allure
import pytest

from lib.util.config_loader import load_yaml


@pytest.mark.ui
class TestLogin:

    @pytest.mark.parametrize("params", load_yaml('case_data/ui/login.yaml')['cases'])
    def test_login(self, params, login_page):
        allure.dynamic.title(params["title"])

        with allure.step("打开登录页面"):
            login_page.open()

        with allure.step(f"输入用户名: {params['username']} 和 密码: {params['password']}"):
            login_page.login(params['username'], params['password'])

        with allure.step("断言登录结果"):
            # 建立映射关系
            message_getters = {
                "success": login_page.get_success_message,
                "empty_username": login_page.get_empty_username_msg,
                "empty_password": login_page.get_empty_password_msg,
                "error": login_page.get_error_message,
            }

            # 动态调用对应的方法
            actual_msg = message_getters[params["expect_type"]]()
            assert params["expect"] in actual_msg
