#@File   : .py
#@Time   : 2025/9/15 17:51
#@Author : 
#@Software: PyCharm
import allure
import pytest

from lib.ui.H5.home_page import HomePage

@pytest.mark.ui
@allure.feature("首页模块")
class TestHomePage:
    @allure.story("首页加载")
    @allure.title("验证首页加载成功")
    def test_homepage_load_success(self, home):
        """验证首页加载成功"""
        with allure.step("检查首页关键模块是否展示"):

            assert home.is_banner_displayed(), "首页轮播图未显示"
            assert home.is_brand_section_displayed(), "品牌专区未显示"
            assert home.is_seckill_displayed(), "秒杀专区未显示"
            assert home.is_fresh_goods_displayed(), "新鲜好物未显示"
            assert home.is_hot_recommend_displayed(), "人气推荐未显示"
    @allure.story("搜索功能")
    @allure.title("验证首页点击搜索框跳转到搜索页面")
    def test_search_product(self, home):
        """验证首页搜索功能"""
        with allure.step("验证点击搜索框跳转到搜索页面："):
            home.search_product()
        with allure.step("断言跳转到搜索页面"):
            assert "搜索商品" in home.driver.page_source

    @allure.story("业务场景")
    @allure.title("验证点击轮播图跳转到品牌详情页面")
    def test_click_banner(self, home):
        with allure.step("验证点击轮播图跳转到品牌详情页面："):
            home.click_banner()
        with allure.step("断言验证点击轮播图跳转到品牌详情页面"):
            assert "品牌详情" in home.driver.page_source


    @allure.story("业务场景")
    @allure.title("验证点击通知跳转到通知页面")
    def test_click_message(self, home):
        with allure.step("验证点击通知跳转到通知页面："):
            home.click_message()
            assert "通知" in home.driver.page_source


    @allure.story("导航栏")
    @allure.title("验证点击分类按钮跳转成功")
    def test_click_category(self, home):
        with allure.step("点击分类按钮"):
            home.click_category()
        with allure.step("断言跳转分类页面"):
            assert "分类" in home.driver.page_source

    @allure.story("导航栏")
    @allure.title("验证点击购物车跳转成功")
    def test_click_cart(self, home):
        with allure.step("点击购物车按钮"):
            home.go_to_cart()
        with allure.step("断言跳转购物车页面"):
            assert "购物车" in home.driver.page_source

    @allure.story("导航栏")
    @allure.title("验证点击我的跳转成功")
    def test_click_mine(self, home):
        with allure.step("点击我的按钮"):
            home.click_mine()
        with allure.step("断言跳转个人中心页面"):
            assert "我的" in home.driver.page_source

    @allure.story("业务场景")
    @allure.title("验证品牌制造商直供点击跳转成功")
    def test_click_brand(self, home):
        with allure.step("点击品牌制造商直供"):
            home.click_brand()
        with allure.step("断言跳转品牌制造商直供页面"):
            assert "推荐品牌列表" in home.driver.page_source

    @allure.story("业务场景")
    @allure.title("验证品牌专区展示数量")
    def test_brand_section_count(self, home):
        with allure.step("获取品牌专区展示数量"):
            brands = home.get_brand_list()
        with allure.step("断言至少有一个品牌"):
            assert len(brands) > 0, "品牌专区未展示任何品牌"

    @allure.story("业务场景")
    @allure.title("验证新鲜好物点击跳转成功")
    def test_fresh_goods(self, home):
        with allure.step("点击新鲜好物"):
            home.click_fresh_goods()
        with allure.step("断言跳转新鲜好物页面"):
            assert "新鲜好物" in home.driver.page_source

    @allure.story("业务场景")
    @allure.title("验证人气推荐点击跳转成功")
    def test_hot_recommend(self, home):
        with allure.step("点击人气推荐"):
            home.click_hot_recommend()
        with allure.step("断言跳转人气推荐页面"):
            assert "人气推荐" in home.driver.page_source

    @allure.story("业务场景")
    @allure.title("验证猜你喜欢的商品展示数量")
    def test_guess_you_like_count(self, home):
        with allure.step("获取猜你喜欢展示数量"):
            like_goods = home.get_guess_you_like_list()
        with allure.step("断言至少有一个商品"):
            assert len(like_goods) > 0, "猜你喜欢未展示任何商品"
