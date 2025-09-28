#@File   : .py
#@Time   : 2025/9/15 17:47
#@Author : 
#@Software: PyCharm
import time

from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage
from lib.util.config_loader import get_config


class LoginPage(BasePage):
    #  定位符
    username_input = (By.XPATH, "//uni-view[4]/uni-view[3]/uni-view[1]//input")  # 用户名输入框
    password_input = (By.XPATH, "//uni-view[4]/uni-view[3]/uni-view[2]//input")  # 密码输入框
    login_button = (By.XPATH, "//uni-button[text()='登录']")  # 登陆按钮
    def __init__(self,driver):
        super().__init__(driver)
        self.url = get_config()['config']['h5']['base_url'] + "pages/public/login"
    def open(self):
        return self.open_url(self.url)

    def set_username(self, username: str):
        self.send_keys(self.username_input, username)

    def set_password(self, password: str):
        self.send_keys(self.password_input, password)

    def click_login(self):
        self.click(self.login_button)


