# @File   : .py
# @Time   : 2023/7/23 22:44
# @Author :
# @Software: PyCharm
import logging
import os
import time

import allure
import pytest

from lib.apilib.formula import Formula
from lib.apilib.login import get_auth_tokens, paas_get_auth_tokens
from functools import wraps

# 获取app登录接口的user_token
@pytest.fixture(scope='session')
def init_admin():
    user_token = get_auth_tokens()
    allure.attach(f"初始化登录的token:{user_token}")
    return user_token
# 获取paas登录接口的user_token
@pytest.fixture(scope='session')
def paas_token():
    user_token = paas_get_auth_tokens()
    return user_token


# 返回Formula对象实例
@pytest.fixture()
def before_formula(init_admin):
    user_token = init_admin
    formula = Formula(user_token)
    return formula



from colorama import Fore, Style, init
from _pytest.terminal import TerminalReporter

# 初始化 colorama
# init(autoreset=True)
# class CustomSummaryReporter:
#     def __init__(self, terminalreporter: TerminalReporter):
#         self.terminalreporter = terminalreporter
#
#     def generate_summary(self):
#         stats = self.terminalreporter.stats
#         total = self.terminalreporter._numcollected
#         passed = len(stats.get('passed', []))
#         failed = len(stats.get('failed', []))
#         error = len(stats.get('error', []))
#         skipped = len(stats.get('skipped', []))
#         xfailed = len(stats.get('xfailed', []))
#         xpassed = len(stats.get('xpassed', []))  # 预期失败但实际通过的用例
#         start_time = self.terminalreporter._sessionstarttime
#         duration = time.time() - start_time
#         duration_str = time.strftime("%H:%M:%S", time.gmtime(duration))
#         desc = f"""
#             api测试用例本次执行情况如下：
#             总用例数为：{total}
#             通过用例数：{passed}
#             失败用例数: {failed}
#             错误用例数：{error}
#             预期失败的用例：{xfailed}
#             预期失败但实际通过的用例：{xpassed}
#             跳过用例数：{skipped}
#             执行时长：{duration_str}
#             测试报告地址：[http://192.168.220.1:60000/index.html](http://192.168.220.1:60000/index.html)
#         """
#         # 使用 colorama 设置颜色和样式，拼接分隔符
#         summary_title = f"{Fore.YELLOW}{Style.BRIGHT}{'-' * 20} Execution Summary {'-' * 20}{Style.RESET_ALL}"
#
#         # 在终端中打印结果
#         self.terminalreporter.write(summary_title + '\n')  # 打印带颜色和分隔符的标题
#         self.terminalreporter.write(f"{Fore.GREEN}{desc}{Style.RESET_ALL}\n")  # 将描述内容设置为绿色
#
#         # 发送描述信息到企业微信
#         send_msg(desc)
#
#
# def pytest_terminal_summary(terminalreporter: TerminalReporter):
#     reporter = CustomSummaryReporter(terminalreporter)
#     reporter.generate_summary()










# # 返回RecordList对象实例
# @pytest.fixture()
# def before_recordList(init_admin):
#     user_token = init_admin
#     recordList = RecordList(user_token)
#     return recordList
# # 返回FormSave对象实例
# @pytest.fixture()
# def before_formSave(paas_token):
#     user_token = paas_token
#     formSave = FormSave(user_token)
#     return formSave

# # Common
# @pytest.fixture(scope='session')
# def before_common(init_admin):
#     common = Common(init_admin)
#     return common
# businessRule
# @pytest.fixture(scope='session')
# def before_businessRule(paas_token):
#     businessRule = BusinessRule(paas_token)
#     return businessRule
# # calendarPromptLight
# @pytest.fixture(scope='session')
# def before_calendarPromptLight(init_admin):
#     CPLight = CalendarPromptLight(init_admin)
#     return CPLight






