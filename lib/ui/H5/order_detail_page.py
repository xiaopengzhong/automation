#@File   : .py
#@Time   : 2025/10/12 16:18
#@Author : 
#@Software: PyCharm

# lib/ui/H5/order_detail_page.py
from selenium.webdriver.common.by import By
from lib.ui.web.base_page import BasePage
from lib.utils.logger import setup_logging

logger = setup_logging("ui")
class OrderDetailPage(BasePage):
    """订单详情页"""

    # ==== 定位符 ====
    page_title = (By.CSS_SELECTOR, ".uni-page-head__title")  # 页面标题
    order_status = (By.CSS_SELECTOR, ".label-text")     # 等待发货
    #receiver_info = (By.CSS_SELECTOR, ".order-content")          # 收货人信息区域
    receiver_name = (By.XPATH, "//uni-text[@class='name']/span")  # 收货人姓名
    receiver_phone = (By.XPATH, "//uni-text[@class='mobile']/span")  # 收货人电话
    receiver_address = (By.XPATH, "//uni-text[@class='address']/span")  # 收货人地址
    product_name = (By.CSS_SELECTOR, ".title span")       # 商品标题
    product_price = (By.CSS_SELECTOR, ".price span")      # 商品价格
    product_quantity = (By.CSS_SELECTOR, ".number span")  # 商品数量
    total_products_price = (By.XPATH, "//uni-text[span='商品合计']/following-sibling::uni-text[@class='cell-tip']/span") # 商品合计
    promotions = (By.XPATH, "//uni-text[span='活动优惠']/following-sibling::uni-text[@class='cell-tip']/span")  # 活动优惠
    coupons = (By.XPATH, "//uni-text[span='优惠卷']/following-sibling::uni-text[@class='cell-tip']/span")  # 优惠卷
    point_deduction = (By.XPATH, "//uni-text[span='积分抵扣']/following-sibling::uni-text[@class='cell-tip']/span")  # 积分抵扣
    remark = (By.XPATH, "//uni-text[span='备注']/following-sibling::uni-text[@class='cell-tip']/span")  # 备注
    order_no = (By.XPATH, "//uni-text[span='订单编号']/following-sibling::uni-text[@class='cell-tip']/span")  # 订单编号
    submit_time = (By.XPATH, "//uni-text[span='提交时间']/following-sibling::uni-text[@class='cell-tip']/span")  # 提交时间
    pay_method = (By.XPATH, "//uni-text[span='支付方式']/following-sibling::uni-text[@class='cell-tip']/span")  # 支付方式
    actual_amount_paid = (By.XPATH, "//uni-text[span='实付金额']/following-sibling::uni-text[@class='cell-tip']/span")  # 实付金额
    payment_time = (By.XPATH, "//uni-text[span='付款时间']/following-sibling::uni-text[@class='cell-tip']/span")  # 付款时间

    # ==== 页面加载判断 ====
    def is_order_detail_loaded(self):
        """判断订单详情页是否加载完成"""
        result = self.is_element_present(self.page_title)
        logger.info(f"订单详情页加载状态: {result}")
        return result

    # ==== 页面信息获取 ====
    def get_order_status(self):
        return self.get_text_safe(self.order_status)

    def get_product_name(self):
        return self.get_text_safe(self.product_name)

    def get_product_price(self):
        return self.get_text_safe(self.product_price)

    def get_total_products_price(self):
        return self.get_text_safe(self.total_products_price)

    def get_promotions(self):
        return self.get_text_safe(self.promotions)

    def get_coupons(self):
        return self.get_text_safe(self.coupons)

    def get_point_deduction(self):
        return self.get_text_safe(self.point_deduction)

    def get_remark(self):
        return self.get_text_safe(self.remark)

    def get_order_no(self):
        return self.get_text_safe(self.order_no)

    def get_submit_time(self):
        return self.get_text_safe(self.submit_time)

    def get_pay_method(self):
        return self.get_text_safe(self.pay_method)

    def get_actual_amount_paid(self):
        return self.get_text_safe(self.actual_amount_paid)

    def get_payment_time(self):
        return self.get_text_safe(self.payment_time)

    def get_receiver_info(self):
        """获取收货人信息"""
        return {
            "name": self.get_text_safe(self.receiver_name),
            "phone": self.get_text_safe(self.receiver_phone),
            "address": self.get_text_safe(self.receiver_address)
        }

    # ==== 信息整合 ====
    def get_order_basic_info(self):
        """获取订单基础信息"""
        info = {
            "status": self.get_order_status(),
            "order_id": self.get_order_no(),
            "submit_time": self.get_submit_time(),
            "payment_method": self.get_pay_method(),
            "actual_paid": self.get_actual_amount_paid(),
        }
        logger.info(f"订单基础信息: {info}")
        return info

    def get_product_info(self):
        """获取订单商品信息"""
        info = {
            "name": self.get_product_name(),
            "price": self.get_product_price(),
            "quantity": self.get_text_safe(self.product_quantity)
        }
        logger.info(f"商品信息: {info}")
        return info

    def get_order_detail(self):
        """组合所有信息"""
        detail = {
            **self.get_order_basic_info(),
            **self.get_product_info(),
            **self.get_receiver_info(),
            "promotions": self.get_promotions(),
            "coupons": self.get_coupons(),
            "point_deduction": self.get_point_deduction(),
            "remark": self.get_remark(),
            "total_products_price": self.get_total_products_price(),
            "payment_time": self.get_payment_time(),
        }
        logger.info(f"完整订单详情: {detail}")
        return detail


    def get_order_detail_info(self):
        """收集页面展示信息"""
        return {
            "order_no": self.get_text_safe(self.order_no),
            "status": self.get_text_safe(self.order_status),
            "receiver_name": self.get_text_safe(self.receiver_name),
            "receiver_phone": self.get_text_safe(self.receiver_phone),
            "receiver_address": self.get_text_safe(self.receiver_address),
            "product_name": self.get_text_safe(self.product_name),
            "product_price": self.get_text_safe(self.product_price),
            "product_quantity": self.get_text_safe(self.product_quantity),
            "actual_amount_paid": self.get_text_safe(self.actual_amount_paid),
        }