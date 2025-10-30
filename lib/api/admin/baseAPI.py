#@File   : .py
#@Time   : 2024/8/26 23:40
#@Author : 
#@Software: PyCharm

#lib/api/baseAPI.py
import logging
import time
import os
import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout, RequestException
from urllib3.util.retry import Retry
from lib.utils.config_loader import load_yaml, get_config


class APIError(Exception):
    """自定义 API 异常，包含请求和响应信息"""

    def __init__(self, message, response=None):
        super().__init__(message)
        self.response = response
        self.status_code = response.status_code if response else None
        self.body = None
        try:
            if response and response.text:
                self.body = response.json()
        except Exception:
            self.body = response.text


class BaseAPI:
    """API 请求基类（增强版）"""

    _global_config = None  # 类变量缓存全局配置，避免重复加载

    def __init__(self, auth_token=None, payload_file=None, env="prod"):
        """
        Args:
            auth_token (str, optional): 认证token
            payload_file (str, optional): 预定义请求体的YAML文件路径
            env (str): 运行环境（dev/test/stage/prod）
        """
        # 首次初始化时加载全局配置
        if BaseAPI._global_config is None:
            BaseAPI._global_config = get_config()["config"]

        # 多环境支持

        self.base_url = BaseAPI._global_config["api"]["base_url"]

        self.payload = self._load_payload(payload_file)
        self.session = self._create_session(auth_token)
        self.logger = logging.getLogger(self.__class__.__name__)

        # 日志最大长度（可在配置里设置）
        self.max_log_len = BaseAPI._global_config["api"].get("max_log_len", 1000)

    def _create_session(self, auth_token):
        """创建带重试机制和默认头的Session"""
        session = requests.Session()
        retries = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[502, 503, 504]
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))

        default_headers = {"Content-Type": "application/json;charset=UTF-8"}
        if auth_token:
            default_headers["X-User-Token"] = auth_token
        session.headers.update(default_headers)
        return session

    def _log_request_response(self, response):
        """安全记录请求和响应信息（自动脱敏 + 截断）"""
        safe_headers = {
            k: ("***" if "token" in k.lower() else v)
            for k, v in response.request.headers.items()
        }
        self.logger.info(f"Request: {response.request.method} {response.request.url}")
        self.logger.info(f"Request headers: {safe_headers}")
        if response.request.body:
            body_preview = str(response.request.body)[:self.max_log_len]
            self.logger.info(f"Request body: {body_preview}")
        self.logger.info(f"Response status code: {response.status_code}")
        if response.content:
            body_preview = response.text[:self.max_log_len]
            self.logger.info(f"Response body: {body_preview}")

    def _handle_exceptions(self, response):
        """统一处理HTTP异常"""
        try:
            response.raise_for_status()
        except (HTTPError, Timeout, RequestException) as err:
            self.logger.error(f"请求异常: {err}")
            raise APIError(f"请求失败: {err}", response)
        return response

    def _load_payload(self, payload_file):
        """加载预定义的请求体模板"""
        if payload_file and os.path.exists(payload_file):
            return load_yaml(payload_file)
        return {}

    def request(self, method, endpoint, threshold=1, **kwargs):
        """统一请求入口

        Returns:
            dict: 统一封装的响应结果
        """
        url = f"{self.base_url}{endpoint}"
        try:
            start_time = time.time()
            response = self.session.request(method, url, timeout=10, **kwargs)
            execution_time = time.time() - start_time

            self.logger.info(f"接口 {endpoint} 执行时间: {execution_time:.2f} 秒")
            if threshold and execution_time > threshold:
                self.logger.warning(f"⚠️ 接口 {endpoint} 响应超时: {execution_time:.2f} 秒")

            self._log_request_response(response)
            response = self._handle_exceptions(response)

            # 统一返回结构
            try:
                body = response.json()
            except Exception:
                body = response.text

            return {
                "status_code": response.status_code,
                "elapsed_time": execution_time,
                "body": body,
                "raw": response  # 保留原始 Response 以兼容旧代码
            }

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise

    # 快捷方法
    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
