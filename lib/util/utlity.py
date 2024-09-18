#@File   : .py
#@Time   : 2024/9/7 0:17
#@Author : 
#@Software: PyCharm
import logging
import os
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
if __name__ == '__main__':
    # print(read_data(file_path="../../case_data/crud.yaml"))
    # print(read_data(file_path="../../case_data/formula.yaml"))
    send_msg("hello")