#@File   : .py
#@Time   : 2025/9/25 19:06
#@Author : 
#@Software: PyCharmfrom lib.ui.base_page import BasePage
from selenium.webdriver.common.by import By

from lib.ui.web.base_page import BasePage
from lib.utils.logger import setup_logging

logger = setup_logging("ui")
class CheckoutPage(BasePage):
    """结算页 Page 封装"""

    # 元素定位符
    confirm_order_text = (By.XPATH, "//uni-page-head/div[1]/div[2]/div")
    submit_order_button = (By.XPATH, "//uni-page-body/uni-view/uni-view[4]/uni-text")
    pay_btn = (By.XPATH, "//uni-app/uni-modal/div[2]/div[3]/div[2]")
    cancel_pay_btn = (By.XPATH, "//uni-app/uni-modal/div[2]/div[3]/div[1]")
    actual_payment_text = (By.XPATH, "//uni-view[contains(text(),'实付款')]")
    address_info = (By.XPATH, "//uni-view[contains(text(),'广东省')]")  # 地址
    remark_input = (By.XPATH, "//textarea")  # 备注输入框

    def is_checkout_page_loaded(self):
        """检查结算页是否加载成功"""
        logger.info("等待结算页加载完成...")
        return self.is_element_present(self.confirm_order_text)

    def get_actual_payment_amount(self):
        """获取实付款金额"""
        text = self.get_text(self.actual_payment_text)
        if text:
            try:
                amount = float(text.replace("实付款 ¥", "").strip())
                logger.info(f"当前实付款金额为：{amount}")
                return amount
            except ValueError:
                logger.error(f"金额解析失败: {text}")
        return None

    def input_remark(self, remark):
        """输入备注信息"""
        self.send_keys(self.remark_input, remark)
        logger.info(f"输入备注：{remark}")

    def submit_order(self):
        """点击提交订单"""
        self.click(self.submit_order_button)
        logger.info("点击提交订单")

    def confirm_pay_popup_visible(self):
        """判断是否弹出支付确认框"""
        return self.is_element_present(self.pay_btn)

    def confirm_pay(self):
        """点击去支付"""
        self.click(self.pay_btn)
        logger.info("确认支付")

    def cancel_pay(self):
        """点击取消支付"""
        self.click(self.cancel_pay_btn)
        logger.info("取消支付")