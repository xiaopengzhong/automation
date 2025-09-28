#@File   : .py
#@Time   : 2024/9/3 22:49
#@Author : 
#@Software: PyCharm


import pytest

from lib.ui.H5.home_page import HomePage
from lib.ui.web.login_page import LoginPage

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import os

@pytest.fixture(scope="function")
def driver():
    """统一浏览器驱动初始化和销毁"""
    chrome_options = webdriver.ChromeOptions()
    # 如果需要移动端模式
    mobile_emulation = {"deviceName": "iPhone XR"}
    chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

    driver_path = os.path.join(os.path.dirname(__file__), "../../drivers/chromedriver.exe")
    driver_path = os.path.abspath(driver_path)  # 转成绝对路径
    service = Service(driver_path)
    driver = webdriver.Chrome(service=service, options=chrome_options)
    driver.maximize_window()

    yield driver
    driver.quit()

@pytest.fixture()
def login_page(driver):
    page = LoginPage(driver)
    yield page
    page.quit()
@pytest.fixture(scope="function")
def home(driver):
    """每个用例初始化并关闭浏览器"""
    page = HomePage(driver)
    page.open()
    yield page
    page.quit()
