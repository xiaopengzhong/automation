#@File   : .py
#@Time   : 2024/9/3 22:11
#@Author : 
#@Software: PyCharm
# base_page.py
import os
import time
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from lib.util.logger import setup_logging

logger = setup_logging("ui")


class BasePage:
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.timeout = timeout

    # ----------------- 页面操作 -----------------
    def open_url(self, url):
        logger.info(f"打开URL: {url}")
        self.driver.get(url)

    def refresh_page(self):
        logger.info("刷新页面")
        self.driver.refresh()

    def quit(self):
        logger.info("退出浏览器")
        self.driver.quit()

    def close(self):
        logger.info("关闭当前窗口")
        self.driver.close()

    # ----------------- 元素查找 -----------------
    def wait_until_visible(self, locator):
        """等待元素可见"""
        return WebDriverWait(self.driver, self.timeout).until(
            EC.visibility_of_element_located(locator)
        )

    def find_element(self, locator):
        try:
            element = self.wait_until_visible(locator)
            return element
        except Exception as e:
            self._handle_error("find_element", locator, e)

    def find_elements(self, locator):
        try:
            elements = WebDriverWait(self.driver, self.timeout).until(
                EC.presence_of_all_elements_located(locator)
            )
            return elements
        except Exception as e:
            self._handle_error("find_elements", locator, e)

    def is_element_present(self, locator) -> bool:
        try:
            self.find_element(locator)
            return True
        except NoSuchElementException:
            return False

    def get_text(self, locator):
        element = self.wait_until_visible(locator)
        return element.text.strip()

    def is_enabled(self, locator):
        """判断元素是否可用（可点击/可输入）"""
        try:
            element = self.wait_until_visible(locator)
            return element.is_enabled()
        except Exception:
            return False


    # ----------------- 元素操作 -----------------
    def click(self, locator):
        try:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", element)
            WebDriverWait(self.driver, self.timeout).until(
                EC.element_to_be_clickable(locator)
            )
            element.click()
            logger.info(f"点击元素: {locator}")
        except ElementClickInterceptedException:
            element = self.find_element(locator)
            self.driver.execute_script("arguments[0].click();", element)
            logger.warning(f"元素 {locator} 被遮挡，已用 JS 点击代替")
        except Exception as e:
            self._handle_error("click", locator, e)

    def send_keys(self, locator, text):
        try:
            element = self.find_element(locator)
            if element.is_enabled():
                element.clear()
                self.driver.execute_script(
                    "arguments[0].value=''; arguments[0].dispatchEvent(new Event('input'));", element)
                element.send_keys(text)
                logger.info(f"输入文本到 {locator}: {text}")
            else:
                raise Exception(f"元素 {locator} 不可编辑")
        except Exception as e:
            self._handle_error("send_keys", locator, e)

    def enter(self, locator):
        try:
            element = self.find_element(locator)
            element.send_keys(Keys.ENTER)
            logger.info(f"在 {locator} 输入框回车")
        except Exception as e:
            self._handle_error("enter", locator, e)

    def scroll_to_element(self, locator, max_swipes=5):
        for _ in range(max_swipes):
            if self.is_element_present(locator):
                return True
            self.driver.execute_script("window.scrollBy(0,500)")
            time.sleep(1)
        logger.error(f"Element not found after scrolling: {locator}")
        self._capture_screenshot()
        return False

    # ----------------- 错误处理 -----------------
    def _handle_error(self, action, locator, error):
        logger.error(f"{action} 失败，locator={locator}, error={error}")
        self._capture_screenshot()
        allure.attach(self.driver.get_screenshot_as_png(),
                      name=f"{action}_screenshot",
                      attachment_type=allure.attachment_type.PNG)
        allure.attach(str(error),
                      name=f"{action}_error",
                      attachment_type=allure.attachment_type.TEXT)
        raise error

    def _capture_screenshot(self):
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S')
        screenshots_dir = os.path.join('screenshots', time.strftime('%Y-%m-%d'))
        os.makedirs(screenshots_dir, exist_ok=True)
        screenshot_path = os.path.join(screenshots_dir, f'screenshot_{timestamp}.png')
        self.driver.save_screenshot(screenshot_path)
        logger.info(f"截图已保存: {screenshot_path}")
