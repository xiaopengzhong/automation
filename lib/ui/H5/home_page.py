#@File   : .py
#@Time   : 2025/9/9 14:56
#@Author : 
#@Software: PyCharm
import time

from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


from lib.ui.web.base_page import BasePage
from lib.util.config_loader import get_config


class HomePage(BasePage):
    #定位符
    message = (By.XPATH, "//uni-page-head/div/div[3]/div/i")  # 通知
    search_input = (By.XPATH, "//uni-page-head/div/div[2]/uni-input")  # 搜索框
    banner_img = (By.XPATH, "//uni-swiper/div/div/div")  # 首页轮播图
    index_tab = (By.XPATH, "//uni-tabbar/div[1]/div[2]")  # 底部导航栏 - 首页
    category_tab = (By.XPATH, "//uni-tabbar/div[1]/div[3]")  # 底部导航栏 - 分类
    cart_tab = (By.XPATH, "//text()[contains(., '购物车')]/..")  # 底部导航栏 - 购物车
    mine_tab = (By.XPATH, "//text()[contains(., '我的')]/..")  # 底部导航栏 - 我的
    brand_section = (By.CSS_SELECTOR, "uni-view:nth-child(3) > uni-view > uni-text:nth-child(1) > span")  #品牌制造商提供
    seckill_section = (By.XPATH, "//uni-view[5]/uni-view[1]/uni-text[1]/span")  # 秒杀专区
    fresh_goods_section = (By.XPATH, "//uni-view[7]/uni-view/uni-text[1]")  #新鲜好物
    hot_recommend_section = (By.XPATH, "//uni-view[9]/uni-view/uni-text[1]/span")  #人气推荐
    brand_items = (By.XPATH, "//uni-view[4]")  # 品牌专区单个品牌，可根据实际页面改
    guess_you_like = (By.XPATH, "//uni-view[11]/uni-view/uni-text[1]/span")  # 猜你喜欢
    like_goods_items = (By.XPATH, "//uni-view[12]")  # 猜你喜欢的商品列表
    FIRST_PRODUCT = (By.XPATH, "//uni-view[8]/uni-scroll-view//uni-view[1]")  # 首页第一个商品（这里假设是商品列表第一个 item）

    def __init__(self, driver):
        super().__init__(driver)
        self.url = get_config()['config']['h5']['base_url']

    # 页面操作方法
    def open(self):
        """打开首页"""
        self.open_url(self.url)

    def click_search_input(self):
        """点击搜索框  """
        element = self.driver.find_element(*self.search_input)  # 解包 tuple 变成 WebElement
        actions = ActionChains(self.driver)

        actions.move_to_element_with_offset(
            element, 5, element.size['height'] // 2
        ).click().perform()
    def click_message(self):
        """点击通知"""
        self.click(self.message)
    def click_index(self):
        """点击首页"""
        self.click(self.index_tab)

    def click_category(self):
        """点击分类"""
        self.click(self.category_tab)

    def go_to_cart(self):
        """点击购物车"""
        self.click(self.cart_tab)

    def click_mine(self):
        """点击我的"""
        self.click(self.mine_tab)

    def is_banner_displayed(self):
        """检查轮播图是否显示"""
        return self.is_element_present(self.banner_img)
    def click_banner(self):
        """点击轮播图跳转到详情页"""
        self.click(self.banner_img)

    def is_brand_section_displayed(self):
        """检查品牌区是否显示"""
        return self.is_element_present(self.brand_section)
    def click_brand(self):
        """点击品牌制造商直供"""
        self.click(self.brand_section)
    def get_brand_list(self):
        """获取品牌专区的所有品牌元素"""
        return self.find_elements(self.brand_items)


    def is_seckill_displayed(self):
        """检查秒杀专区是否显示"""
        return self.is_element_present(self.seckill_section)

    def is_fresh_goods_displayed(self):
        """检查新鲜好物是否显示"""
        return self.is_element_present(self.fresh_goods_section)
    def click_fresh_goods(self):
        """点击新鲜好物"""
        self.scroll_to_element(self.fresh_goods_section)
        time.sleep(2)
        self.click(self.fresh_goods_section)


    def is_hot_recommend_displayed(self):
        """检查人气推荐是否显示"""
        return self.is_element_present(self.hot_recommend_section)
    def click_hot_recommend(self):
        """点击人气推荐"""
        self.scroll_to_element(self.hot_recommend_section)
        self.click(self.hot_recommend_section)

    def is_guess_you_like_displayed(self):
        """检查猜你喜欢是否显示"""
        return self.is_element_present(self.guess_you_like)
    def get_guess_you_like_list(self):
        """ 获取猜你喜欢的所有商品元素  """
        return self.find_elements(self.like_goods_items)

    def click_first_product(self):
        """点击首页第一个商品"""
        self.click(self.FIRST_PRODUCT)






