#@File   : .py
#@Time   : 2024/9/3 22:11
#@Author : 
#@Software: PyCharm
import os

from selenium import webdriver
from selenium.webdriver import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import allure
import time


class BasePage:
    def __init__(self, browser='chrome', mode='desktop'):


        self.driver = self._init_driver(browser, mode)

        self.driver.implicitly_wait(10)  # 默认隐式等待时间

    def _init_driver(self, browser, mode):
        """
        初始化浏览器驱动，支持桌面和手机模式
        :param browser: 浏览器类型
        :param mode: 浏览器模式
        :return: 浏览器驱动对象
        """
        if browser == 'chrome':
            chrome_options = webdriver.ChromeOptions()

            # 检查是否需要开启手机模式
            if mode == 'mobile':
                mobile_emulation = {"deviceName": "iPhone XR"}
                chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)

            # 启动 Chrome 浏览器
            driver = webdriver.Chrome(options=chrome_options)

        # 可以根据需要添加其他浏览器支持，例如 Firefox, Edge 等
        else:
            raise ValueError(f"Unsupported browser: {browser}")

        return driver



    def open_url(self, url):

        self.driver.get(url)
    def refresh_page(self):
        self.driver.refresh()




    def find_element(self, locator):
        # 查找元素，返回WebElement对象
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(locator)
            )
            return element
        except Exception as e:
            self._capture_screenshot()
            allure.attach(self.driver.get_screenshot_as_png(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            allure.attach(str(e), name="error", attachment_type=allure.attachment_type.TEXT)
            raise

    def click(self, locator):
        # 点击元素
        element = self.find_element(locator)
        element.click()

    def send_keys(self, locator, text):
        # 输入文本
        element = self.find_element(locator)
        element.clear()
        element.send_keys(text)

    # def _capture_screenshot(self):
    #     # 截图并保存
    #     timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
    #     self.driver.save_screenshot(f'screenshot_{timestamp}.png')
    def _capture_screenshot(self):
        """
        截图并将其保存在 screenshots 文件夹中。
        文件名包含当前的时间戳，以确保唯一性。
        """
        # 获取当前时间戳，用于文件命名
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')

        # 定义截图保存的文件夹
        screenshots_dir = 'screenshots'

        # 检查文件夹是否存在，如果不存在则创建
        if not os.path.exists(screenshots_dir):
            os.makedirs(screenshots_dir)

        # 定义截图的完整路径和文件名
        screenshot_path = os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')

        # 截图并保存到指定路径
        self.driver.save_screenshot(screenshot_path)

    def quit(self):
        # 关闭浏览器
        self.driver.quit()
