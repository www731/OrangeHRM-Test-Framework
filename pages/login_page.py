# pages/login_page.py
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage
import allure


class LoginPage(BasePage):
    """OrangeHRM 登录页面对象"""

    # ==================== Locators ====================
    USERNAME_FIELD = (By.NAME, "username")
    PASSWORD_FIELD = (By.NAME, "password")
    LOGIN_BUTTON = (By.XPATH, "//button[@type='submit']")          # 最稳定
    # 备选：LOGIN_BUTTON = (By.CSS_SELECTOR, ".oxd-button--main")  # 也可以

    GLOBAL_ERROR_MESSAGE = (By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/div/div[1]/div[1]/p')
    # 用户名字段的 Required 提示
    USERNAME_REQUIRED = (
    By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[1]/div/span')

    # 密码字段的 Required 提示
    PASSWORD_REQUIRED = (
    By.XPATH, '//*[@id="app"]/div[1]/div/div[1]/div/div[2]/div[2]/form/div[2]/div/span')

    INVALID_CREDENTIALS_MSG = "Invalid credentials"                # 预期错误文本（英文版demo）



    # ==================== Actions ====================

    @allure.step("打开登录页面")
    def open_login_page(self):
        """直接访问登录URL"""
        self.driver.get("https://opensource-demo.orangehrmlive.com/web/index.php/auth/login")
        self.logger.info("已打开登录页面")

    @allure.step("输入用户名: {username}")
    def enter_username(self, username: str):
        self.send_keys(self.USERNAME_FIELD, username)

    @allure.step("输入密码: {password}")
    def enter_password(self, password: str):
        self.send_keys(self.PASSWORD_FIELD, password)

    @allure.step("点击登录按钮")
    def click_login_button(self):
        self.click(self.LOGIN_BUTTON)

    @allure.step("执行完整登录流程")
    def login(self, username: str, password: str):
        """一键登录方法（组合动作）"""
        self.open_login_page()
        self.enter_username(username)
        self.enter_password(password)
        self.click_login_button()
        self.logger.info(f"尝试登录 → 用户名: {username}")

        # 加等待：等页面跳转或错误框出现（最多 10 秒）
        try:
            WebDriverWait(self.driver, 20).until(
                lambda d: "dashboard" in d.current_url.lower() or
                          EC.presence_of_element_located(self.ERROR_MESSAGE)(d)
            )
        except:
            pass  # 不抛异常，继续让断言判断

    @allure.step("获取登录错误消息（全局或字段级）")
    def get_error_message(self) -> str:
        messages = []

        # 检查全局错误（如 Invalid credentials）
        try:
            global_msg_elem = WebDriverWait(self.driver, 5).until(
                EC.visibility_of_element_located(self.GLOBAL_ERROR_MESSAGE)
            )
            global_msg = global_msg_elem.text.strip()
            if global_msg:
                messages.append(global_msg)
                self.logger.info(f"捕获到全局错误: {global_msg}")
        except:
            pass  # 没有全局错误，继续检查字段

        # 检查用户名字段 Required
        try:
            user_req = self.driver.find_element(*self.USERNAME_REQUIRED)
            if user_req.is_displayed() and "Required" in user_req.text:
                messages.append("Username is required")
                self.logger.info("检测到用户名 Required 提示")
        except:
            pass

        # 检查密码字段 Required
        try:
            pwd_req = self.driver.find_element(*self.PASSWORD_REQUIRED)
            if pwd_req.is_displayed() and "Required" in pwd_req.text:
                messages.append("Password is required")
                self.logger.info("检测到密码 Required 提示")
        except:
            pass

        if messages:
            return " | ".join(messages)
        else:
            self.logger.warning("未捕获到任何错误提示")
            return ""

    @allure.step("检查是否登录成功（仪表盘）")
    def is_login_success(self) -> bool:
        try:
            # 等待 URL 包含 dashboard（最多等 15 秒）
            WebDriverWait(self.driver, 45).until(
                lambda d: "dashboard" in d.current_url.lower()
            )
            self.logger.info(f"URL 跳转成功: {self.driver.current_url}")

            # 额外检查页面是否有 "Dashboard" 标题元素（demo 站点的 h6 标签）
            dashboard_title = WebDriverWait(self.driver, 10).until(
                EC.visibility_of_element_located((By.XPATH, "//h6[contains(., 'Dashboard')]"))
            )
            self.logger.info(f"找到 Dashboard 标题: {dashboard_title.text}")
            return True
        except Exception as e:
            self.logger.error(f"登录成功检查失败: {str(e)}")
            self.logger.info(f"当前 URL: {self.driver.current_url}")
            self.logger.info(f"当前 Title: {self.driver.title}")
            return False