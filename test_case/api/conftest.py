# @File   : .py
# @Time   : 2023/7/23 22:44
# @Author :
# @Software: PyCharm
import json
import logging
from typing import Generator, Tuple, List

import allure
import pytest
from lib.api.businessRule import BusinessRule
from lib.api.crud import Crud
from lib.api.formula import Formula
from lib.api.login import get_auth_tokens, paas_get_auth_tokens
from lib.util.config_loader import load_yaml
from lib.util.decorators import rate_limit
from lib.util.logger import setup_logging
#test_case/api/conftest.py



logger = setup_logging("api")
# =========================
# 登录相关 Fixture
# =========================
@pytest.fixture(scope="session")
def admin_token() -> str:
    """获取 app 登录 token"""
    try:
        token = get_auth_tokens()
        allure.attach(json.dumps({"token": token}, ensure_ascii=False), "Admin Token", allure.attachment_type.JSON)
        logger.info("成功获取 Admin Token")
        return token
    except Exception as e:
        logger.exception("获取 Admin Token 失败")
        pytest.exit(f"无法获取 Admin Token: {e}")


@pytest.fixture(scope="session")
def paas_token() -> str:
    """获取 paas 登录 token"""
    try:
        token = paas_get_auth_tokens()
        allure.attach(json.dumps({"token": token}, ensure_ascii=False), "Paas Token", allure.attachment_type.JSON)
        logger.info("成功获取 Paas Token")
        return token
    except Exception as e:
        logger.exception("获取 Paas Token 失败")
        pytest.exit(f"无法获取 Paas Token: {e}")


# =========================
# 对象初始化 Fixture
# =========================
@pytest.fixture(scope="session")
def formula_client(admin_token: str) -> Formula:
    """Formula API 客户端"""
    client = Formula(admin_token)
    logger.info("初始化 Formula 客户端")
    return client


@pytest.fixture(scope="session")
def crud_client(admin_token: str) -> Crud:
    """Crud API 客户端"""
    client = Crud(admin_token)
    allure.attach(json.dumps({"crud": str(client)}, ensure_ascii=False), "初始化 Crud 客户端", allure.attachment_type.JSON)
    logger.info("初始化 Crud 客户端")
    return client


@pytest.fixture(scope="session")
def business_rule_client(paas_token: str) -> BusinessRule:
    """BusinessRule API 客户端"""
    client = BusinessRule(paas_token)
    logger.info("初始化 BusinessRule 客户端")
    return client


# =========================
# 数据准备 Fixture
# =========================
@pytest.fixture()
def add_test_data(crud_client: Crud) -> Generator[Tuple[Crud, List[dict]], None, None]:
    """
    新增多条记录，测试结束后清理
    :return: (crud_client, 创建记录时使用的字段数据)
    """
    created_records: List[str] = []
    payloads: List[dict] = load_yaml(file_path="case_data/add_data.yaml")["fieldData"]

    @rate_limit(wait_time=2)
    def submit_data(payload: dict) -> str:
        result = crud_client.submit(fieldData=payload)
        return result["data"]

    logger.info(f"开始批量创建测试数据: 共 {len(payloads)} 条")
    for payload in payloads:
        try:
            record_id = submit_data(payload)
            created_records.append(record_id)
            logger.info(f"创建成功: record_id={record_id}")
        except Exception as e:
            logger.error(f"创建数据失败: {payload} 错误: {e}")

    allure.attach(json.dumps(created_records, ensure_ascii=False), "新增记录 ID 列表", allure.attachment_type.JSON)
    yield crud_client, payloads

    # 测试结束后清理数据
    if created_records:
        try:
            crud_client.delete(recordIds=created_records)
            allure.attach(json.dumps(created_records, ensure_ascii=False), "删除记录 ID 列表",
                          allure.attachment_type.JSON)
            logger.info(f"清理完毕，删除记录数: {len(created_records)}")
        except Exception as e:
            logger.error(f"清理数据失败: {e}")