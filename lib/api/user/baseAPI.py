#@File   : .py
#@Time   : 2024/8/26 23:40
#@Author : 
#@Software: PyCharm


# lib/api/user/baseAPI.py

import time

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout, RequestException
from urllib3.util.retry import Retry
from lib.utils.config_loader import load_yaml, get_config
from lib.utils.logger import setup_logging


class BaseAPI:
    """企业级 API 请求基类"""

    _global_config = None

    def __init__(self, auth_token=None, payload_file=None, default_timeout=10, default_retries=3):
        self.logger = setup_logging("api")
        if BaseAPI._global_config is None:
            BaseAPI._global_config = get_config().get("config", {})

        self.base_url = BaseAPI._global_config.get("api", {}).get("base_url", "")

        self.payload = self._load_payload(payload_file)
        self.session = self._create_session(auth_token, default_retries)
        self.default_timeout = default_timeout




    def _create_session(self, auth_token, retries):
        session = requests.Session()
        retry_strategy = Retry(
            total=retries,
            backoff_factor=1,
            status_forcelist=[502, 503, 504],
            allowed_methods=["HEAD", "GET", "POST", "PUT", "DELETE", "OPTIONS", "PATCH"]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)

        headers = {"Content-Type": "application/json;charset=UTF-8"}
        if auth_token:
            headers["authorization"] = auth_token
        session.headers.update(headers)
        return session


    def _load_payload(self, payload_file):
        """加载类对应的 payload，如果不存在直接抛异常"""
        if not payload_file:
            return {}
        data = load_yaml(payload_file)
        cls_name = self.__class__.__name__
        if cls_name not in data:
            raise KeyError(f"YAML 文件中缺少类 {cls_name} 对应的 key")
        payload = data[cls_name]
        if not isinstance(payload, dict):
            raise ValueError(f"{cls_name} 对应的 payload 必须是字典")
        self.logger.debug(f"成功加载 payload: {payload}")
        return payload

    def _log_request_response(self, response, elapsed):
        """记录请求与响应"""
        # 日志请求的基本信息
        self.logger.info(f"[{response.request.method}] {response.request.url} 耗时: {elapsed:.2f}s")
        self.logger.info(f"请求头: {response.request.headers}")

        # 判断请求体是否存在，并打印请求体
        if response.request.body:
            # 如果请求体是字节类型（bytes），则解码为字符串
            body_str = response.request.body.decode("utf-8") if isinstance(response.request.body, bytes) else str(
                response.request.body)
            self.logger.info(f"请求体: {body_str}")
        else:
            self.logger.debug("请求体为空")

        # 打印响应状态码
        self.logger.info(f"响应状态码: {response.status_code}")

        # 打印响应体
        self.logger.info(f"响应体: {response.text}")

        # 响应时间告警
        threshold = getattr(response, "_threshold", 1)
        if elapsed > threshold:
            self.logger.warning(f"⚠️ 接口 {response.request.url} 响应超时: {elapsed:.2f}s")

    def _handle_exceptions(self, response):
        """统一处理异常"""
        try:
            response.raise_for_status()
        except (HTTPError, Timeout, RequestException) as e:
            self.logger.error(f"请求异常: {e}, 响应体: {response.text if response else '无'}")
            raise
        return response

    def request(self, method, endpoint, threshold=None, timeout=None, **kwargs):
        """统一请求入口"""
        url = f"{self.base_url}{endpoint}"
        timeout = timeout or self.default_timeout
        threshold = threshold or 1  # 默认超时阈值
        try:
            start = time.time()
            response = self.session.request(method, url, timeout=timeout, **kwargs)
            elapsed = time.time() - start
            setattr(response, "_threshold", threshold)

            self._log_request_response(response, elapsed)
            return self._handle_exceptions(response)

        except Exception as e:
            self.logger.error(f"请求 {url} 发生错误: {e}")
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
