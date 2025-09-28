#@File   : .py
#@Time   : 2024/8/30 22:41
#@Author : 
#@Software: PyCharm
# lib/api/crud.py
from lib.api.baseAPI import BaseAPI
import copy


class Crud(BaseAPI):
    """
    CRUD操作高级封装类（继承自BaseAPI）

    提供对特定业务对象的增删改查操作：
    - 提交记录 submit
    - 查询记录详情 detail
    - 删除记录 delete
    - 更新记录 edit
    - 查询列表 list_records
    - 获取全量记录 get_all_records
    """

    def __init__(self, token=None, object_name="yxpm__CustomObject0148__c"):
        """
        初始化 CRUD 客户端

        Args:
            token (str, optional): API认证令牌
            object_name (str, optional): 操作对象名，可扩展多对象
        """
        super().__init__(auth_token=token)
        self.object_name = object_name

    # ---------------- 内部方法 ----------------
    def _check_response(self, response):
        """
        校验接口返回值，统一处理异常

        Args:
            response: requests.Response 对象

        Returns:
            dict: JSON 数据

        Raises:
            ValueError: 接口返回错误码或异常内容
        """
        resp_json = response.json()
        if resp_json.get("code") != 200:
            raise ValueError(f"接口异常: {resp_json}")
        return resp_json

    def _get_payload(self, key, **kwargs):
        """
        获取深拷贝 payload 并合并动态参数

        Args:
            key (str): payload key，如 submit/edit/list
            **kwargs: 动态参数

        Returns:
            dict: 合并后的 payload
        """
        payload = copy.deepcopy(self.payload[key])
        payload.update(kwargs)
        return payload

    # ---------------- CRUD方法 ----------------
    def submit(self, **kwargs):
        """提交新记录"""
        url = f'/api-engine-mid/v1/form/{self.object_name}/2024083017002443504002/record/submit'
        payload = self._get_payload('submit', **kwargs)
        response = self.post(endpoint=url, json=payload)
        return self._check_response(response)

    def detail(self, **kwargs):
        """查询记录详情"""
        url = '/api-engine-mid/v2/page/record/detail'
        payload = self._get_payload('detail', **kwargs)
        response = self.post(endpoint=url, json=payload)
        return self._check_response(response)

    def delete(self, **kwargs):
        """删除指定记录"""
        url = f'/api-engine-mid/v1/form/{self.object_name}/record/delete'
        payload = self._get_payload('delete', **kwargs)
        response = self.post(endpoint=url, json=payload)
        return self._check_response(response)

    def edit(self, _rid, **kwargs):
        """更新现有记录"""
        url = f'/api-engine-mid/v1/form/{self.object_name}/2024083017002443504002/record/{_rid}/update'
        payload = self._get_payload('edit', **kwargs)
        response = self.post(endpoint=url, json=payload)
        return self._check_response(response)

    def list_records(self, **kwargs):
        """分页查询记录列表"""
        url = '/api-engine-mid/v2/page/record/list'
        payload = self._get_payload('list', **kwargs)
        response = self.post(endpoint=url, json=payload)
        return self._check_response(response)

    def get_all_records(self, page_size=20, **kwargs):
        """
        获取所有记录，自动分页

        Args:
            page_size (int, optional): 每页条数
            **kwargs: list_records 接口其他过滤条件

        Returns:
            list: 所有记录数组
        """
        all_data = []
        page = 1

        while True:
            resp = self.list_records(page=page, page_size=page_size, **kwargs)
            data = resp.get("data", [])
            all_data.extend(data)
            if len(data) < page_size:
                break
            page += 1

        return all_data
