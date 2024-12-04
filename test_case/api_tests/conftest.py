# @File   : .py
# @Time   : 2023/7/23 22:44
# @Author :
# @Software: PyCharm
import json
import logging
import os
import time

import allure
import pytest

from lib.apilib.businessRule import BusinessRule
from lib.apilib.crud import Crud
from lib.apilib.formula import Formula
from lib.apilib.login import get_auth_tokens, paas_get_auth_tokens
from functools import wraps
# 获取 logger 实例
from lib.util.utlity import read_data, rate_limit

logger = logging.getLogger()

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
# 返回Crud对象
@pytest.fixture(scope='session')
def get_crud(init_admin):
    """Fixture: 初始化并返回 Crud 对象"""
    crud = Crud(init_admin)
    logger.info("初始化 Crud 对象")
    # 使用 allure 附件记录初始化的 Crud 对象
    allure.attach(json.dumps({"crud": str(crud)}, indent=4), name="初始化Crud对象",
                  attachment_type=allure.attachment_type.JSON)
    return crud
# businessRule
@pytest.fixture(scope='session')
def get_businessRule(paas_token):
    businessRule = BusinessRule(paas_token)
    return businessRule

# 新增21条记录后并删除
@pytest.fixture(scope='session')
def add_data(get_crud):
    """Fixture: 新增多条数据，后置操作清理数据"""
    created_records = []
    add_payloads = read_data(file_path='case_data/add_data.yaml')['fieldData']

    @rate_limit(wait_time=2)
    def submit_data(payload):
        response = get_crud.submit(fieldData=payload)
        return response['data']

    for payload in add_payloads:
        record_id = submit_data(payload)
        created_records.append(record_id)
        logger.info(f"Created record ID: {record_id}")

    allure.attach(str(created_records), "新增记录的ID", allure.attachment_type.JSON)
    yield get_crud, add_payloads

    # 清理已创建的记录
    get_crud.delete(recordIds=created_records)
    allure.attach(str(created_records), "删除的记录ID", allure.attachment_type.JSON)
    logger.info("清理完毕，已删除记录")




