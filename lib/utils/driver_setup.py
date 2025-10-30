#@File   : .py
#@Time   : 2024/9/9 22:07
#@Author : 
#@Software: PyCharm
# utils/driver_setup.py

from appium import webdriver



def get_driver():
    desired_caps = {
        "platformName": "Android",
        "deviceName": "127.0.0.1：62001",
        "appPackage": "com.tencent.mm",
        "appActivity": "com.tencent.mm.ui.LauncherUI",
        "automationName": "UiAutomator2"
    }

    driver = webdriver.Remote("http://127.0.0.1:4723/wd/hub", desired_caps)
    driver.implicitly_wait(10)
    return driver


