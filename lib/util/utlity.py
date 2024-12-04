#@File   : .py
#@Time   : 2024/9/7 0:17
#@Author : 
#@Software: PyCharm
import json
import logging
import os
import time
from functools import wraps

import allure
import requests
import yaml
from typing import Optional
# 配置日志
def setup_logging():
    # 指定日志文件夹路径
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)  # 如果文件夹不存在则创建

    # 完整的日志文件路径
    log_file = os.path.join(log_dir, "test.log")

    # 创建一个日志记录器
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)  # 设置全局日志级别为 INFO

    # 创建一个文件处理器用于写入日志，指定编码为 UTF-8
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)  # 文件处理器级别

    # 创建一个日志格式器并将其添加到处理器
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # 添加文件处理器到 logger
    logger.addHandler(file_handler)

    # 添加一个控制台处理器以便同时输出到控制台
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # 刷新日志
    for handler in logger.handlers:
        handler.flush()

# 发送消息
def send_msg(result: str) -> Optional[requests.Response]:
    """
    发送测试报告到企业微信
    """
    url = os.getenv("WECHAT_WEBHOOK_URL","https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=48325383-d35a-496b-b907-abe53e91843a")
    headers = {'Content-Type': 'application/json;charset=utf-8'}
    data_text = {
        "msgtype": "markdown",
        "markdown": {
            "content": result
        }
    }

    logger = logging.getLogger(__name__)
    try:
        response = requests.post(url=url, json=data_text, headers=headers)
        response.raise_for_status()
        logger.info("消息发送成功")
        return response
    except requests.exceptions.RequestException as e:
        logger.error(f"消息发送失败: {e}")
        return None

# 读取数据
def read_data(file_path="conf/api_config.yaml"):
    logger = logging.getLogger(__name__)
    try:
        with open(file_path, encoding="utf-8") as file_handle:
            data = yaml.safe_load(file_handle)
    except FileNotFoundError:
        logger.error(f"Error: File '{file_path}' not found.")
        data = {}
    except yaml.YAMLError as exc:
        logger.error(f"Error in YAML file '{file_path}': {exc}")
        data = {}

    return data
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
# 全局工具方法
def attach_log(data, title, attachment_type=allure.attachment_type.JSON):
    """
    封装 Allure 的日志附件方法
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data, indent=4, ensure_ascii=False)
    allure.attach(data, name=title, attachment_type=attachment_type)

if __name__ == '__main__':
    # print(read_data(file_path="../../conf/api_config.yaml"))
    print(read_data(file_path="../../case_data/add_data.yaml"))
    # print(read_data(file_path="../../case_data/formula.yaml"))
    # send_msg("hello")