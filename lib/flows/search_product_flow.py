#@File   : .py
#@Time   : 2025/9/29 2:20
#@Author : 
#@Software: PyCharm
from lib.flows.login_flow import LoginFlow
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.search_product_page import SearchProductPage





class SearchProductFlow:
    """商品搜索流程"""

    def __init__(self, driver):
        self.driver = driver

    def search_product(self, username, password, keyword):
        """
        完整业务流：
        1. 登录
        2. 打开首页
        3. 进入搜索页
        4. 输入关键词并搜索
        5. 返回搜索结果页对象
        """
        # 1. 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        # 2. 打开首页
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")

        # 3. 进入搜索页（假设首页有搜索入口）
        home.click_search_input()

        # 4. 输入关键词并点击搜索
        search_page = SearchProductPage(self.driver)
        search_page.set_enter_product_name(keyword)
        search_page.click_search_btn()


        return search_page
