#@File   : .py
#@Time   : 2025/9/28 20:35
#@Author : 
#@Software: PyCharm
import time

from lib.ui.H5.login_page import LoginPage



class LoginFlow:
    """登录流程"""

    def __init__(self, driver):
        self.driver = driver

    def login(self, username: str, password: str, open_page: bool = True):
        login_page = LoginPage(self.driver)
        if open_page:
            login_page.open()  # 默认执行，支持手动关闭
        login_page.set_username(username)
        login_page.set_password(password)
        time.sleep(1)
        login_page.click_login()
        time.sleep(0.5)
        return login_page
