#@File   : .py
#@Time   : 2025/8/11 18:14
#@Author : 
#@Software: PyCharm
# 发送消息
import logging
import os
from typing import Optional

import requests


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
