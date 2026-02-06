# pages/base_page.py

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from utils.logger import get_logger
import allure

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 15)          # 默认等15秒
        self.logger = get_logger(self.__class__.__name__)  # 每个页面有自己的日志

    # 通用点击方法（所有页面都能用）
    @allure.step("点击元素 {locator}")
    def click(self, locator):
        try:
            elem = self.wait.until(EC.element_to_be_clickable(locator))
            elem.click()
            self.logger.info(f"成功点击元素: {locator}")
        except TimeoutException:
            self.logger.error(f"点击失败，元素 {locator} 超时未可点击")
            raise
        except Exception as e:
            self.logger.error(f"点击 {locator} 时出错: {str(e)}")
            raise

    # 通用输入方法
    @allure.step("在 {locator} 输入文字: {text}")
    def send_keys(self, locator, text):
        try:
            elem = self.wait.until(EC.visibility_of_element_located(locator))
            elem.clear()
            elem.send_keys(text)
            self.logger.info(f"在 {locator} 输入: {text}")
        except TimeoutException:
            self.logger.warning(f"元素 {locator} 可见等待超时，尝试直接 find_element")
            elem = self.driver.find_element(*locator)
            elem.clear()
            elem.send_keys(text)
        except Exception as e:
            self.logger.error(f"输入失败 {locator}: {str(e)}")
            raise

    # 通用获取文字
    @allure.step("获取元素 {locator} 的文字")
    def get_text(self, locator):
        try:
            elem = self.wait.until(EC.visibility_of_element_located(locator))
            text = elem.text
            self.logger.info(f"获取到文字: {text}")
            return text
        except Exception as e:
            self.logger.error(f"获取文字失败 {locator}: {str(e)}")
            raise

    # 可以继续加更多通用方法，比如：is_element_visible、scroll_to_element 等