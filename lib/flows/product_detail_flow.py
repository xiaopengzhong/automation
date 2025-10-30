#@File   : .py
#@Time   : 2025/9/29 22:50
#@Author : 
#@Software: PyCharm
from lib.flows.login_flow import LoginFlow
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.product_detail_page import ProductDetailPage
from lib.ui.H5.product_search_page import ProducSearchtPage


class ProductDetailFlow:
    """商品详情业务流"""

    def __init__(self, driver):
        self.driver = driver

    def view_product(self, username, password, keyword):
        """
        完整业务流：
        1. 登录
        2. 打开首页
        3. 进入搜索页
        4. 输入关键词搜索
        5. 点击商品进入详情
        6. 返回商品详情页对象
        """
        # 1. 登录
        login_flow = LoginFlow(self.driver)
        login_flow.login(username=username, password=password)

        # 2. 打开首页
        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")

        # 3. 点击搜索框进入搜索页
        home.click_search_input()

        # 4. 输入关键词搜索
        search_page = ProducSearchtPage(self.driver)
        search_page.set_enter_product_name(keyword)
        search_page.click_search_btn()

        # 5. 点击搜索结果商品

        search_page.click_product()


        # 6. 返回商品详情对象
        return ProductDetailPage(self.driver)
    def collect_product(self):
        """收藏商品"""
        product_detail_page = ProductDetailPage(self.driver)
        product_detail_page.click_collect()
    def go_home(self):
        """回到首页"""
        product_detail_page = ProductDetailPage(self.driver)
        product_detail_page.click_go_home()

