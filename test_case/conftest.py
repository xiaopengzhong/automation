#@File   : .py
#@Time   : 2024/9/6 23:06
#@Author : 
#@Software: PyCharm


import time

# 初始化计数器
from lib.util.logger import setup_logging
from lib.util.send_mssage import send_msg

ui_passed = 0
ui_failed = 0
ui_skipped = 0
ui_duration = 0.0
ui_total = 0  # UI 总用例数

api_passed = 0
api_failed = 0
api_skipped = 0
api_duration = 0.0
api_total = 0  # API 总用例数

# 用于存储每个测试用例的开始时间
test_start_times = {}

def pytest_collection_modifyitems(items):
    """调整 API 和 UI 测试用例的执行顺序"""
    ui_tests = []
    api_tests = []

    for item in items:
        if "ui" in item.keywords:
            ui_tests.append(item)
        elif "api" in item.keywords:
            api_tests.append(item)

    # 更新总用例数
    global ui_total, api_total
    ui_total = len(ui_tests)
    api_total = len(api_tests)

    # 先执行 API 测试，再执行 UI 测试
    items[:] = api_tests + ui_tests

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

def send_report(test_type, passed, failed, skipped, total, duration, report_url):
    """发送报告"""
    if total == 0:
        return  # 如果用例总数为 0，则不发送报告

    duration_str = time.strftime("%H:%M:%S", time.gmtime(duration))
    desc = f"""
        {test_type} 测试用例本次执行情况如下：
        总用例数：{total}
        通过用例数：{passed}
        失败用例数：{failed}
        跳过用例数：{skipped}
        执行时长：{duration_str}
        测试报告地址：[{report_url}]({report_url})
    """
    send_msg(desc)

def pytest_terminal_summary(terminalreporter, exitstatus, config):
    global ui_passed, ui_failed, ui_skipped, ui_duration, ui_total
    global api_passed, api_failed, api_skipped, api_duration, api_total

    # 发送API测试报告
    send_report(
        test_type="API",
        total=api_total,
        passed=api_passed,
        failed=api_failed,
        skipped=api_skipped,
        duration=api_duration,
        report_url="http://192.168.220.1:60000/api_report.html"
    )

    # 发送UI测试报告
    send_report(
        test_type="UI",
        total=ui_total,
        passed=ui_passed,
        failed=ui_failed,
        skipped=ui_skipped,
        duration=ui_duration,
        report_url="http://192.168.220.1:60000/ui_report.html"
    )




def pytest_configure(config):
    # 调用 setup_logging 来设置日志
    setup_logging()