#@File   : .py
#@Time   : 2025/8/15 1:42
#@Author : 
#@Software: PyCharm
def get_all_pages(api_func, page_size=20, **kwargs):
    """
    分页获取全部数据

    :param api_func: 支持 page 参数的接口调用函数
    :param page_size: 每页大小，默认 20
    :param kwargs: 额外传给 api_func 的参数
    :return: list, 所有数据
    """
    page = 1
    all_data = []

    while True:
        resp = api_func(page=page, **kwargs)
        if not isinstance(resp, dict):
            raise ValueError("接口返回值必须是 dict 类型")

        data = resp.get("data", [])
        if not isinstance(data, list):
            raise ValueError("接口返回的 'data' 字段必须是 list 类型")

        all_data.extend(data)

        # 如果返回的数据不足一页，说明已经拉完
        if len(data) < page_size:
            break

        page += 1

    return all_data
