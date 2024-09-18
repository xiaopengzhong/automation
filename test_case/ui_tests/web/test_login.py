#@File   : .py
#@Time   : 2024/9/3 22:50
#@Author : 
#@Software: PyCharm
import pytest



from lib.uilib.web.loginPage import LoginPage
from lib.uilib.web.phone_loginPage import Phone_LoginPage

import allure
import pytest


@pytest.mark.ui
class TestLogin:

    @pytest.mark.parametrize("username, password, expected_text", [
        ('14912345678', 'Aa123456', "小明测试应用"),
        ('14912345678', '123456', "帐号或密码错误，请重新输入"),
        # 可以添加更多的用户名和密码组合
    ])
    @allure.title("桌面端登录测试: 用户名 {username} 密码 {password}")
    @allure.description("验证桌面端登录功能的正确性，检查成功或失败后的消息提示。")
    def test_login(self, username, password, expected_text):
        login_page = LoginPage(mode='desktop')
        with allure.step(f"打开登录页面 (Desktop mode)"):
            login_page.open()

        with allure.step(f"输入用户名: {username}，密码: {password} 并登录"):
            login_page.login(username, password)

        if expected_text == "帐号或密码错误，请重新输入":
            with allure.step(f"验证错误提示消息是否显示"):
                error_element = login_page.get_error_message()
                assert error_element.is_displayed(), "预期的错误消息未显示"
                assert error_element.text.strip() == expected_text, f"期望显示：{expected_text}，但实际显示：{error_element.text.strip()}"
        else:
            with allure.step("验证登录是否成功"):
                success_element = login_page.get_success_message()
                assert success_element.is_displayed(), "登录失败或成功消息未显示"
                assert success_element.text.strip() == expected_text, f"期望显示: {expected_text}, 但实际显示: {success_element.text.strip()}"

    @pytest.mark.parametrize("username, password, expected_text", [
        ('14912345678', 'Aa123456', "ZXP(别动)"),
        ('14912345678', '123456', "帐号或密码错误，请重新输入"),
        # 可以添加更多的用户名和密码组合
    ])
    @allure.title("手机端登录测试: 用户名 {username} 密码 {password}")
    @allure.description("验证手机端登录功能的正确性，检查成功或失败后的消息提示。")
    def test_phone_login(self, username, password, expected_text):
        login_page = Phone_LoginPage(mode='mobile')
        with allure.step("打开登录页面 (Mobile mode)"):
            login_page.open()

        with allure.step("刷新登录页面"):
            login_page.refresh()

        with allure.step(f"输入用户名: {username}，密码: {password} 并登录"):
            login_page.login(username, password)

        if expected_text == "帐号或密码错误，请重新输入":
            with allure.step("验证错误提示消息是否显示"):
                error_element = login_page.get_error_message()
                assert error_element.is_displayed(), "预期的错误消息未显示"
                assert error_element.text.strip() == expected_text, f"期望显示：{expected_text}，但实际显示：{error_element.text.strip()}"
        else:
            with allure.step("验证登录是否成功"):
                success_element = login_page.get_success_message()
                assert success_element.is_displayed(), "登录失败或成功消息未显示"
                assert success_element.text.strip() == expected_text, f"期望显示: {expected_text}, 但实际显示: {success_element.text.strip()}"
