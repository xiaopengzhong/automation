#@File   : .py
#@Time   : 2024/9/10 12:06
#@Author : 
#@Software: PyCharm
import pytest

from lib.ui.mobile.login_page import LoginPage
from lib.util.driver_setup import get_driver


@pytest.fixture(scope="function")
def setup():
    driver = get_driver()
    yield driver
    driver.quit()
@pytest.mark.parametrize("username, password, expected_text", [
        ('14912345678', 'Aa123456', "ZXP(别动)"),
        ('14912345678', '123456', "帐号或密码错误，请重新输入"),
        # 可以添加更多的用户名和密码组合
    ])
def test_login_with_invalid_credentials(setup, username, password, expected_text):
    login_page = LoginPage(setup)
    login_page.enter_username(username)
    login_page.enter_password(password)
    login_page.click_login()

    if expected_text == "帐号或密码错误，请重新输入":
        error_element = login_page.get_error_message()
        assert error_element.is_displayed(), "预期的错误消息为显示"
        assert error_element.text.strip() == expected_text, f"期望显示：{expected_text}，但实际显示：{error_element.text.strip()}"
    else:
        # 检查登录是否成功
        success_element = login_page.get_success_message()

        # 断言：元素是否显示
        assert success_element.is_displayed(), "登录失败或成功消息未显示"
