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
from lib.util.config_loader import load_yaml, get_config


class BaseAPI:
    """API 请求基类（封装公共请求逻辑）"""

    _global_config = None  # 类变量缓存全局配置，避免重复加载

    def __init__(self, auth_token=None, payload_file=None):
        """初始化API客户端

        Args:
            auth_token (str, optional): 认证token，自动添加到请求头
            payload_file (str, optional): 预定义请求体的YAML文件路径
        """
        # 首次初始化时加载全局配置（后续实例共享）
        if BaseAPI._global_config is None:
            BaseAPI._global_config = get_config()["config"]  # 获取合并后的最终配置

        self.base_url = BaseAPI._global_config["api"]["base_url"]  # 从配置读取API根地址
        self.payload = self._load_payload(payload_file)  # 加载预定义请求体
        self.session = self._create_session(auth_token)  # 创建定制化Session
        self.logger = logging.getLogger(self.__class__.__name__)  # 每个子类使用独立日志器

    def _create_session(self, auth_token):
        """创建带重试机制和默认头的Session

        Args:
            auth_token: 认证token，会添加到请求头

        Returns:
            requests.Session: 预配置的会话对象
        """
        session = requests.Session()

        # 配置重试策略（对502/503/504状态码重试3次，退避时间1秒）
        retries = Retry(
            total=3,
            backoff_factor=1,  # 退避系数 (delay = backoff_factor * (2^(retry-1)))
            status_forcelist=[502, 503, 504]  # 强制重试的状态码
        )
        session.mount("http://", HTTPAdapter(max_retries=retries))
        session.mount("https://", HTTPAdapter(max_retries=retries))

        # 设置默认请求头
        default_headers = {"Content-Type": "application/json;charset=UTF-8"}
        if auth_token:
            default_headers["X-User-Token"] = auth_token  # 动态添加认证头
        session.headers.update(default_headers)

        return session

    def _log_request_response(self, response):
        """安全记录请求和响应信息（自动脱敏token）

        Args:
            response: requests.Response对象
        """
        # 脱敏处理headers中的token字段
        safe_headers = {
            k: ("***" if "token" in k.lower() else v)
            for k, v in response.request.headers.items()
        }

        self.logger.info(f"Request: {response.request.method} {response.request.url}")
        self.logger.info(f"Request headers: {safe_headers}")
        if response.request.body:
            self.logger.info(f"Request body: {response.request.body}")
        self.logger.info(f"Response status code: {response.status_code}")
        if response.content:
            self.logger.info(f"Response body: {response.text}")

    def _handle_exceptions(self, response):
        """统一处理HTTP异常

        Args:
            response: requests.Response对象

        Returns:
            Response: 如果状态码正常则返回原响应

        Raises:
            HTTPError: 4xx/5xx状态码异常
            Timeout: 请求超时
            RequestException: 其他请求异常
        """
        try:
            response.raise_for_status()  # 自动抛出4xx/5xx异常
        except (HTTPError, Timeout, RequestException) as err:
            self.logger.error(f"请求异常: {err}")
            raise  # 重新抛出异常给调用方
        return response

    def _load_payload(self, payload_file):
        """加载预定义的请求体模板

        Args:
            payload_file: YAML文件路径

        Returns:
            dict: 解析后的字典，文件不存在时返回空字典
        """
        if payload_file and os.path.exists(payload_file):
            return load_yaml(payload_file)
        return {}

    def request(self, method, endpoint, threshold=1, **kwargs):
        """统一请求入口

        Args:
            method: HTTP方法（GET/POST等）
            endpoint: API路径（会自动拼接base_url）
            threshold: 响应时间阈值（秒），超时记录警告
            **kwargs: 透传给requests的参数（如json/data/params）

        Returns:
            Response: 响应对象

        Raises:
            Exception: 所有请求异常
        """
        url = f"{self.base_url}{endpoint}"  # 拼接完整URL

        try:
            # 计时开始
            start_time = time.time()

            # 发起请求（默认超时10秒）
            response = self.session.request(method, url, timeout=10, **kwargs)

            # 计算耗时
            execution_time = time.time() - start_time
            self.logger.info(f"接口 {endpoint} 执行时间: {execution_time:.2f} 秒")

            # 超时警告
            if threshold and execution_time > threshold:
                self.logger.warning(f"⚠️ 接口 {endpoint} 响应超时: {execution_time:.2f} 秒")

            # 记录请求详情
            self._log_request_response(response)

            # 异常处理
            return self._handle_exceptions(response)

        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise  # 继续向上抛出

    # 快捷方法
    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)