#@File   : .py
#@Time   : 2025/8/11 17:59
#@Author : 
#@Software: PyCharm
#lib/utils/logger.py
import json
import os
import logging
from logging.handlers import TimedRotatingFileHandler
import datetime

import allure


def setup_logging(log_type: str = "api", backup_days: int = 30):
    """
    初始化日志记录器（企业级，根目录 logs）

    :param log_type: 日志类型，可选 "api" 或 "ui"
    :param backup_days: 保留历史日志天数
    :return: logger 对象
    """
    if log_type not in ("api", "ui"):
        raise ValueError("log_type 必须是 'api' 或 'ui'")

    # 项目根目录（假设这个文件在 lib/utils/logger_util.py）
    current_file = os.path.abspath(__file__)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(current_file)))  # 根目录

    # 日志目录
    log_dir = os.path.join(BASE_DIR, "logs", log_type)
    os.makedirs(log_dir, exist_ok=True)

    # 按天生成文件名
    log_file = os.path.join(log_dir, f"{datetime.date.today().strftime('%Y-%m-%d')}_{log_type}.log")

    # 创建 logger
    logger = logging.getLogger(log_type)
    logger.setLevel(logging.INFO)
    logger.propagate = False  # 防止重复打印日志

    # 文件处理器 - 每天自动生成新日志，保留 backup_days
    # 只有在 logger 还没有 handler 时才添加
    if not logger.handlers:
        file_handler = TimedRotatingFileHandler(
            log_file,
            when="midnight",
            interval=1,
            backupCount=backup_days,
            encoding="utf-8",
            delay=True
        )
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    return logger


def attach_log(data, title, attachment_type=allure.attachment_type.JSON):
    """
    封装 Allure 的日志附件方法
    """
    if isinstance(data, (dict, list)):
        data = json.dumps(data, indent=4, ensure_ascii=False)
    allure.attach(data, name=title, attachment_type=attachment_type)