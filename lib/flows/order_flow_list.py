#@File   : .py
#@Time   : 2025/10/5 17:18
#@Author : 
#@Software: PyCharm
# lib/ui/flows/order_flow_list.py
from lib.flows.login_flow import LoginFlow
from lib.ui.H5.cart_page import CartPage
from lib.ui.H5.checkout_page import CheckoutPage
from lib.ui.H5.home_page import HomePage
from lib.ui.H5.order_list_page import OrderListPage
from lib.ui.H5.pay_success_page import PaySuccessPage
from lib.ui.H5.payment_page import PayMentPage
from lib.ui.H5.product_detail_page import ProductDetailPage
from lib.ui.H5.product_search_page import ProducSearchtPage
from lib.utils.logger import setup_logging

logger=setup_logging("ui")
class OrderFlow:
    """订单业务流（创建订单 + 查看订单列表）"""

    def __init__(self, driver):
        self.driver = driver

    def create_and_pay_order(self, username, password, product_name):
        """完整下单流程"""
        logger.info(f"=== 开始执行下单流程：{username} 购买 {product_name} ===")
        login_flow = LoginFlow(self.driver)
        login_flow.login(username, password)

        home = HomePage(self.driver)
        home.open_url("http://localhost:8060/#/")
        home.click_search_input()

        search_page = ProducSearchtPage(self.driver)
        search_page.set_enter_product_name(product_name)
        search_page.click_search_btn()
        search_page.click_product()

        product_page = ProductDetailPage(self.driver)
        product_page.click_add_to_cart()
        product_page.click_go_to_cart()

        cart_page = CartPage(self.driver)
        cart_page.go_checkout()

        checkout_page = CheckoutPage(self.driver)
        checkout_page.submit_order()
        checkout_page.confirm_pay()

        payment_page = PayMentPage(self.driver)
        payment_page.click_confirm_pay_btn()

        pay_success_page = PaySuccessPage(self.driver)
        pay_success_page.click_check_order_btn()

        order_page = OrderListPage(self.driver)
        assert order_page.is_order_page_loaded(), "订单列表页加载失败"
        logger.info("✅ 订单流程执行成功，已进入订单列表页")
        return order_page

    def get_latest_order_info(self, username, password, product_name=None):
        """获取最新订单信息（可复用旧订单）"""
        order_page = self.create_and_pay_order(username, password, product_name)
        info = order_page.get_first_order_info()
        logger.info(f"最新订单信息：{info}")
        return info