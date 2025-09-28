#@File   : .py
#@Time   : 2024/9/9 21:43
#@Author : 
#@Software: PyCharm
# pages/base_page.py


from appium.webdriver.webdriver import WebDriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import logging
import time

class BasePage:
    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.logger = logging.getLogger(self.__class__.__name__)
        self.driver.implicitly_wait(10)

    def find_element(self, by, value, timeout=10):
        """查找单个元素并处理异常"""
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_element_located((by, value))
            )
            self.logger.info(f"Element found: {by}, {value}")
            return element
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Element not found: {by}, {value}, Exception: {e}")
            self.take_screenshot("find_element_error")
            raise

    def find_elements(self, by, value, timeout=10):
        """查找多个元素"""
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.visibility_of_all_elements_located((by, value))
            )
            self.logger.info(f"Elements found: {by}, {value}")
            return elements
        except (TimeoutException, NoSuchElementException) as e:
            self.logger.error(f"Elements not found: {by}, {value}, Exception: {e}")
            self.take_screenshot("find_elements_error")
            raise

    def click(self, by, value, timeout=10):
        """点击元素"""
        element = self.find_element(by, value, timeout)
        element.click()
        self.logger.info(f"Clicked on element: {by}, {value}")

    def send_keys(self, by, value, text, timeout=10):
        """发送文本到输入框"""
        element = self.find_element(by, value, timeout)
        element.clear()
        element.send_keys(text)
        self.logger.info(f"Sent keys to element: {by}, {value}, Text: {text}")

    def is_element_displayed(self, by, value, timeout=10):
        """检查元素是否显示"""
        try:
            element = self.find_element(by, value, timeout)
            displayed = element.is_displayed()
            self.logger.info(f"Element displayed: {by}, {value} - {displayed}")
            return displayed
        except:
            self.logger.info(f"Element not displayed: {by}, {value}")
            return False

    def get_text(self, by, value, timeout=10):
        """获取元素文本"""
        element = self.find_element(by, value, timeout)
        text = element.text
        self.logger.info(f"Text from element: {by}, {value} - {text}")
        return text

    def swipe(self, start_x, start_y, end_x, end_y, duration=1000):
        """滑动操作"""
        self.driver.swipe(start_x, start_y, end_x, end_y, duration)
        self.logger.info(f"Swiped from ({start_x}, {start_y}) to ({end_x}, {end_y})")

    def scroll_to_element(self, by, value, max_swipes=5):
        """滚动页面直到元素可见"""
        for _ in range(max_swipes):
            if self.is_element_displayed(by, value):
                return
            self.swipe(500, 1500, 500, 1000)  # 根据具体设备调整滑动位置
            time.sleep(1)
        self.logger.error(f"Element not found after scrolling: {by}, {value}")
        self.take_screenshot("scroll_to_element_error")

    def go_back(self):
        """返回上一个页面"""
        self.driver.back()
        self.logger.info("Navigated back")

    def take_screenshot(self, name):
        """截图并保存到指定目录"""
        timestamp = time.strftime("%Y%m%d-%H%M%S")
        filename = f"screenshots/{name}_{timestamp}.png"
        self.driver.save_screenshot(filename)
        self.logger.info(f"Screenshot saved as {filename}")

    def wait_for_page_to_load(self, timeout=10):
        """等待页面完全加载"""
        try:
            WebDriverWait(self.driver, timeout).until(
                lambda d: d.execute_script("return document.readyState") == "complete"
            )
            self.logger.info("Page loaded completely")
        except TimeoutException:
            self.logger.error("Page did not load within timeout")
            self.take_screenshot("page_load_timeout")

    def handle_alert(self, accept=True):
        """处理系统弹窗"""
        try:
            alert = WebDriverWait(self.driver, 5).until(EC.alert_is_present())
            if accept:
                alert.accept()
                self.logger.info("Alert accepted")
            else:
                alert.dismiss()
                self.logger.info("Alert dismissed")
        except TimeoutException:
            self.logger.info("No alert present")
