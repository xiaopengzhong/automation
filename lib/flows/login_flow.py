#@File   : .py
#@Time   : 2025/9/28 20:35
#@Author : 
#@Software: PyCharm
import time

from lib.ui.H5.login_page import LoginPage
from lib.ui.web.base_page import BasePage
from lib.util.config_loader import get_config


class LoginFlow:
    def __init__(self, driver):
        self.driver = driver

    def login(self, username: str, password: str):
        login_page = LoginPage(self.driver)
        login_page.open()
        login_page.set_username(username)
        login_page.set_password(password)
        login_page.click_login()
        time.sleep(1)
        return login_page
