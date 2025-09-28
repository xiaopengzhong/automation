#@File   : .py
#@Time   : 2024/9/8 19:37
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage
from lib.util.config_loader import get_config

# lib/ui/login_page.py
class LoginPage(BasePage):
    # 页面定位符（集中管理，便于维护）
    username_input = (By.NAME, "username")  # 用户名输入框
    password_input = (By.NAME, "password")  # 密码输入框
    login_button = (By.CSS_SELECTOR, "button.el-button.el-button--primary")  # 登陆按钮
    success_message = (By.XPATH, "//*[@id='app']/div/div[2]/ul/div[2]/span/span/span[1]/span")  # 登陆成功跳转仪表盘
    error_message = (By.XPATH, "//div[@role='alert']//p[@class='el-message__content']")  # 密码错误登陆失败提示
    empty_username = (By.XPATH, "//*[@id='app']/div/div[1]/div/form/div[2]/div/div[2]")  # 用户名为空提示
    empty_password = (By.XPATH, "//div[@class='el-form-item__error']")  # 密码为空提示

    def __init__(self, browser='chrome', mode='desktop'):
        super().__init__(browser, mode)
        self.url = get_config()['config']['ui']['base_url']

    # 页面操作方法
    def open(self):
        """打开登录页面"""
        self.open_url(self.url)



    def set_username(self, username: str):
        self.send_keys(self.username_input, username)

    def set_password(self, password: str):
        self.send_keys(self.password_input, password)

    def click_login(self):
        self.click(self.login_button)

    # 获取页面信息
    def get_success_message(self) -> str:
        return self.find_element(self.success_message).text

    def get_error_message(self) -> str:
        return self.find_element(self.error_message).text

    def get_empty_username_msg(self) -> str:
        return self.find_element(self.empty_username).text

    def get_empty_password_msg(self) -> str:
        return self.find_element(self.empty_password).text

    # 业务流（封装完整登录动作）
    def login(self, username: str, password: str):
        """执行完整登录操作，返回提示信息"""

        # 再输入用户名密码
        self.set_username(username)
        self.set_password(password)
        self.click_login()

