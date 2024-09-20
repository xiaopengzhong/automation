#@File   : .py
#@Time   : 2024/8/26 23:40
#@Author : 
#@Software: PyCharm
import logging
import time

import requests
from requests.adapters import HTTPAdapter
from requests.exceptions import HTTPError, Timeout, RequestException
from urllib3.util.retry import Retry

from conf.env import host
from lib.util.utlity import read_data


class BaseAPI:
    def __init__(self, auth_token=None):
        self.base_url = host  # 请替换为实际的 host
        self.payload = self._load_payload()
        self.session = self._create_session(auth_token)
        self.logger = logging.getLogger(self.__class__.__name__)  # 直接获取类级别的 logger

    def _create_session(self, auth_token):
        session = requests.Session()
        retries = Retry(total=3, backoff_factor=1, status_forcelist=[502, 503, 504])
        session.mount('http://', HTTPAdapter(max_retries=retries))
        session.mount('https://', HTTPAdapter(max_retries=retries))

        if auth_token:
            session.headers.update({
                "Content-Type": "application/json;charset=UTF-8",
                "Cookie": "_bl_uid=qdlFeiX0y1FdXe1wkg6I5sd6n8da",  # 注意处理敏感信息
                "X-User-Token": auth_token
            })
        return session

    def _log_request_response(self, response):
        # 确保日志不会记录敏感数据
        self.logger.info(f"Request: {response.request.method} {response.request.url}")
        self.logger.info(f"Request headers: {response.request.headers}")
        if response.request.body:
            self.logger.info(f"Request body: {response.request.body}")
        self.logger.info(f"Response status code: {response.status_code}")
        if response.content:
            self.logger.info(f"Response body: {response.text}")

    def _handle_exceptions(self, response):
        try:
            response.raise_for_status()
        except HTTPError as http_err:
            self.logger.error(f"HTTP error occurred: {http_err}")
            raise  # Raise the exception to be handled by the calling function
        except Timeout as timeout_err:
            self.logger.error(f"Timeout error occurred: {timeout_err}")
            raise
        except RequestException as req_err:
            self.logger.error(f"Request error occurred: {req_err}")
            raise
        return response

    def _load_payload(self):
        current_name = self.__class__.__name__
        # read_data 函数的实现应当能正确加载对应的 payload
        return read_data().get(current_name, {})

    def request(self, method, endpoint, threshold=1, **kwargs):
        url = f"{self.base_url}{endpoint}"
        try:
            start_time = time.time()
            response = self.session.request(method, url, timeout=10, **kwargs)
            execution_time = time.time() - start_time
            self.logger.info(f"接口 {endpoint} 执行时间: {execution_time:.2f} 秒")
            if threshold and execution_time > threshold:
                logging.warning(f"警告: 接口 {endpoint} 响应时间超出阈值: {execution_time:.2f} 秒")
            self._log_request_response(response)
            return self._handle_exceptions(response)
        except Exception as e:
            self.logger.error(f"An error occurred: {e}")
            raise

    def get(self, endpoint, **kwargs):
        return self.request("GET", endpoint, **kwargs)

    def post(self, endpoint, **kwargs):
        return self.request("POST", endpoint, **kwargs)

    def put(self, endpoint, **kwargs):
        return self.request("PUT", endpoint, **kwargs)

    def delete(self, endpoint, **kwargs):
        return self.request("DELETE", endpoint, **kwargs)
