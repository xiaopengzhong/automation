#@File   : .py
#@Time   : 2025/8/11 18:19
#@Author : 
#@Software: PyCharm
import logging

import time
from functools import wraps


# 自定义装饰器，用于控制接口调用频率
def rate_limit(wait_time=2):  # 外层函数，接收一个参数 wait_time，用于指定等待时间（默认为2秒）
    def decorator(func):  # 内层函数，接收一个函数作为参数，这个函数就是要被装饰的目标函数
        @wraps(func)  # 使用 functools.wraps 保持原函数的元数据，例如函数名和文档字符串
        def wrapper(*args, **kwargs):  # 包装函数，用于包裹目标函数
            result = func(*args, **kwargs)  # 执行目标函数，并获取其返回值
            time.sleep(wait_time)  # 在目标函数执行后等待指定的时间（wait_time 秒）
            return result  # 返回目标函数的执行结果
        return wrapper  # 返回包装后的函数
    return decorator  # 返回装饰器


# 装饰器，用于记录执行时间
PERFORMANCE_THRESHOLD = 2.0  # 默认性能阈值
def record_execution_time(threshold=PERFORMANCE_THRESHOLD):
    def decorator(func):
        def wrapper(*args, **kwargs):
            start_time = time.time()
            response = func(*args, **kwargs)
            execution_time = time.time() - start_time

            logging.info(f"接口执行时间: {execution_time:.2f} 秒")

            if execution_time > threshold:
                logging.warning(f"警告: 接口响应时间超出阈值: {execution_time:.2f} 秒")

            return response
        return wrapper
    return decorator
