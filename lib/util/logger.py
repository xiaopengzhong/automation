#@File   : .py
#@Time   : 2025/8/11 17:59
#@Author : 
#@Software: PyCharm
#lib/util/logger.py
import json

import allure


import os
import logging

def setup_logging(log_type: str = "api"):
    """
    初始化日志记录器
    :param log_type: 日志类型，可选 "api" 或 "ui"
    :return: logger 对象
    """
    if log_type not in ("api", "ui"):
        raise ValueError("log_type 必须是 'api' 或 'ui'")

    log_dir = os.path.join("logs", log_type)
    os.makedirs(log_dir, exist_ok=True)

    log_file = os.path.join(log_dir, f"{log_type}_test.log")

    logger = logging.getLogger(log_type)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # 文件处理器
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # 控制台处理器
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    for handler in logger.handlers:
        handler.flush()

    return logger

def attach_log(data, title, attachment_type=allure.attachment_type.JSON):
    """
    封装 Allure 的日志附件方法
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data, indent=4, ensure_ascii=False)
    allure.attach(data, name=title, attachment_type=attachment_type)