#@File   : .py
#@Time   : 2024/9/6 23:06
#@Author : 
#@Software: PyCharm
from lib.util.utlity import setup_logging, send_msg

import pytest
import time

# 初始化计数器
ui_passed = 0
ui_failed = 0
ui_skipped = 0
ui_duration = 0.0

api_passed = 0
api_failed = 0
api_skipped = 0
api_duration = 0.0

# 用于存储每个测试用例的开始时间
test_start_times = {}

def pytest_runtest_setup(item):
    """在测试用例执行前记录开始时间"""
    test_start_times[item.nodeid] = time.time()

def pytest_runtest_makereport(item, call):
    """根据测试结果更新计数器和累积执行时长"""
    global ui_passed, ui_failed, ui_skipped, ui_duration
    global api_passed, api_failed, api_skipped, api_duration

    if call.when == "call":
        # 计算测试用例的执行时长
        start_time = test_start_times.pop(item.nodeid, None)
        if start_time:
            duration = time.time() - start_time
            if "ui" in item.keywords:
                ui_duration += duration
                if call.excinfo is None:
                    ui_passed += 1
                else:
                    ui_failed += 1
            elif "api" in item.keywords:
                api_duration += duration
                if call.excinfo is None:
                    api_passed += 1
                else:
                    api_failed += 1
    elif call.when == "setup":
        if call.excinfo is not None:
            if "ui" in item.keywords:
                ui_skipped += 1
            elif "api" in item.keywords:
                api_skipped += 1

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global ui_passed, ui_failed, ui_skipped, ui_duration
    global api_passed, api_failed, api_skipped, api_duration

    # 格式化时长
    ui_duration_str = time.strftime("%H:%M:%S", time.gmtime(ui_duration))
    api_duration_str = time.strftime("%H:%M:%S", time.gmtime(api_duration))
    # 生成API测试结果描述字符串
    api_desc = f"""
        API 测试用例本次执行情况如下：
        通过用例数：{api_passed}
        失败用例数：{api_failed}
        跳过用例数：{api_skipped}
        执行时长：{api_duration_str}
        测试报告地址：[http://192.168.220.1:60000/api_report.html](http://192.168.220.1:60000/api_report.html)
        """
    send_msg(api_desc)

    # 生成UI测试结果描述字符串
    ui_desc = f"""
    UI 测试用例本次执行情况如下：
    通过用例数：{ui_passed}
    失败用例数：{ui_failed}
    跳过用例数：{ui_skipped}
    执行时长：{ui_duration_str}
    测试报告地址：[http://192.168.220.1:60000/ui_report.html](http://192.168.220.1:60000/ui_report.html)
    """



    # 分别打印UI和API测试统计结果
    terminalreporter.write("\n" + ui_desc, purple=True)
    terminalreporter.write("\n" + api_desc, purple=True)


    # 分别发送UI和API测试结果
    send_msg(ui_desc)



def pytest_configure(config):
    # 调用 setup_logging 来设置日志
    setup_logging()