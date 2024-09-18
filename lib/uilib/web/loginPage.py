#@File   : .py
#@Time   : 2024/9/8 19:37
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.uilib.web.BasePage import BasePage


class LoginPage(BasePage):
    def __init__(self, browser='chrome', mode='desktop'):
        super().__init__(browser, mode)
        self.url = "https://apps.youxin.cloud/#/login"

        self.username_input = (By.XPATH, "//input[@type='text' and @placeholder='请输入帐号']")
        self.password_input = (By.XPATH, "//input[@type='password' and @placeholder='请输入密码']")
        self.login_button = (By.XPATH, "//button[span[text()='登录']]")
        self.success_message = (By.XPATH, "//*[@id='app']/div/div[1]/div[1]/div/div[2]/span[1]")
        self.error_message = (By.XPATH, "//div[@class='el-alert__content']/p[1]")

    def open(self):
        """打开登录页面"""
        self.open_url(self.url)



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
        self.set_username(username)
        self.set_passwprd(password)
        self.click_login()
