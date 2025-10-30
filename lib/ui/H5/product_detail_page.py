#@File   : .py
#@Time   : 2025/9/29 22:31
#@Author : 
#@Software: PyCharm
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage


class ProductDetailPage(BasePage):
    """商品详情页 Page Object"""

    add_to_cart_btn = (By.XPATH, "//uni-button[contains(text(),'加入购物车')]")  # 加入购物车按钮
    go_to_cart_btn = (By.XPATH, "//uni-page-body//uni-view[8]/uni-navigator[2]")  # 去购物车页面按钮
    buy_now_btn = (By.XPATH, "//uni-button[contains(text(),'立即购买')]")  # 立即购买按钮
    product_title = (By.XPATH, "//uni-page-body//uni-view[2]//uni-text[1]/span")  # 商品标题
    product_price = (By.XPATH, "//uni-page-body//uni-view[2]//uni-view[1]//uni-text[2]/span")  # 商品价格
    collect_btn = (By.XPATH, "//uni-page-body//uni-view[8]/uni-view[1]")  # 收藏按钮
    collect_tip = (By.XPATH, "/uni-app/uni-toast/div/p")  # 收藏提示
    go_home_btn = (By.XPATH, "//uni-page-body//uni-view[8]/uni-navigator[1]")  # 回首页按钮
    go_login_btn = (By.XPATH, "//uni-modal/div[2]/div[3]/div[2]")  # 去登陆按钮
    canncel_btn = (By.XPATH, "//uni-modal/div[2]/div[3]/div[1]")  # 取消按钮

    def __init__(self, driver):
        super().__init__(driver)

    # ---------------- 操作方法 ----------------
    def click_add_to_cart(self):
        self.click(self.add_to_cart_btn)
    def click_go_to_cart(self):
        self.click(self.go_to_cart_btn)

    def click_buy_now(self):
        self.click(self.buy_now_btn)

    def click_go_to_login(self):
        self.click(self.go_login_btn)

    def click_cancel_login(self):
        self.click(self.canncel_btn)

    def click_collect(self):
        self.click(self.collect_btn)

    def click_go_home(self):
        self.click(self.go_home_btn)

    # ---------------- 断言方法 ----------------
    def get_product_title(self):
        return self.get_text(self.product_title)

    def get_product_price(self):
        return self.get_text(self.product_price)

    def get_collect_tip(self):
        return self.get_text(self.collect_tip)



