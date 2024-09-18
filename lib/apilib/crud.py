#@File   : .py
#@Time   : 2024/8/30 22:41
#@Author : 
#@Software: PyCharm
from lib.apilib.baseAPI import BaseAPI


class Crud(BaseAPI):
    def __init__(self, token=None):
        super().__init__(token)
    def submit(self,**kwargs):
        url = '/api-engine-mid/v1/form/yxpm__CustomObject0148__c/2024083017002443504002/record/submit'
        payload = self.payload['submit']
        self.logger.info(f"更新前的请求参数{payload}")
        payload.update(kwargs)

        respose = self.post(endpoint=url, json=payload)
        return respose.json()
    def detail(self,**kwargs):
        url = '/api-engine-mid/v2/page/record/detail'
        payload = self.payload['detail']
        self.logger.info(f"更新前的请求参数{payload}")
        payload.update(kwargs)

        reponse = self.post(endpoint=url, json=payload)
        return reponse.json()
    def delete(self,**kwargs):
        url = '/api-engine-mid/v1/form/yxpm__CustomObject0148__c/record/delete'
        payload = self.payload['delete']
        self.logger.info(f"更新前的请求参数{payload}")
        payload.update(kwargs)

        reponse = self.post(endpoint=url, json=payload)
        return reponse.json()



