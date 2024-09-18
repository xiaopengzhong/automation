#@File   : .py
#@Time   : 2024/9/10 17:15
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.uilib.web.BasePage import BasePage
class Phone_LoginPage(BasePage):
    def __init__(self, browser='chrome', mode='desktop'):
        super().__init__(browser, mode)
        self.url = "https://apps.youxin.cloud/#/"
        self.password_input_button = (By.XPATH, "//uni-button[text()='密码登录']")
        self.username_input = (By.XPATH, "//input[@class='uni-input-input']")
        self.password_input = (By.XPATH, "//input[@type='password' and @class='uni-input-input']")
        self.login_button = (By.XPATH, "//uni-button[@class='m_button login_btn' and text()='登录']")
        self.success_message = (By.XPATH, "//*[@id='app']/uni-app/uni-page/uni-page-wrapper/uni-page-body/uni-view/uni-view[1]/uni-view/uni-view/uni-view/uni-view[1]/uni-view[1]/uni-view")
        self.error_message = (By.XPATH, "//uni-view[@class='form_error m_cred']")

    def open(self):
        """打开登录页面"""
        self.open_url(self.url)
    def refresh(self):
        self.refresh_page()
    def click_password_input_button(self):
        self.click(self.password_input_button)

    def set_username(self, username: str):
        """输入用户名"""
        self.send_keys(self.username_input, username)

    def set_passwprd(self, password: str):
        """输入密码"""
        self.send_keys(self.password_input, password)

    def click_login(self):
        """点击登录按钮"""
        self.click(self.login_button)

    def get_success_message(self):
        """获取登录成功后的信息"""
        return self.find_element(self.success_message)

    def get_error_message(self):
        """获取登录失败后的信息"""
        return self.find_element(self.error_message)

    def login(self, username: str, password: str):
        """执行登录操作"""
        self.click_password_input_button()
        self.set_username(username)
        self.set_passwprd(password)
        self.click_login()
