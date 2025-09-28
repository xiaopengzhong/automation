#@File   : .py
#@Time   : 2024/9/10 12:04
#@Author : 
#@Software: PyCharm
# pages/login_page.py
from selenium.webdriver.common.by import By

from lib.ui.mobile.base_page import BasePage



class LoginPage(BasePage):
    # 定位元素的方式可以根据具体应用进行调整
    username_input = (By.ID, "com.example.app:id/username")
    password_input = (By.ID, "com.example.app:id/password")
    login_button = (By.ID, "com.example.app:id/login_button")
    error_message = (By.ID, "com.example.app:id/error_message")

    def enter_username(self, username):
        self.send_keys(*self.username_input, text=username)

    def enter_password(self, password):
        self.send_keys(*self.password_input, text=password)

    def click_login(self):
        self.click(*self.login_button)

    def get_error_message(self):
        return self.get_text(*self.error_message)

