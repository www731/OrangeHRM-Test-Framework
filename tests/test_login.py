# tests/test_login.py
import pytest
import allure
from pages.login_page import LoginPage
from utils.logger import get_logger

logger = get_logger(__name__)


# 从 conftest.py 注入 driver fixture
# 你也可以通过 --browser chrome/firefox 切换浏览器


@allure.feature("登录模块")
@allure.story("用户认证")
@allure.tag("smoke", "login")
class TestLogin:

    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.login_page = LoginPage(driver)
        yield
        # 可选：清理（但登录页不需要特别清理）

    @allure.title("TC01 - 正常登录（正确用户名 + 正确密码）")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_valid_credentials(self):
        """预期：成功进入 Dashboard"""
        self.login_page.login("Admin", "admin123")
        assert self.login_page.is_login_success(), "登录后未跳转到仪表盘"
        logger.info("正常登录测试通过")

    # TC02 - 错误密码（预期全局 Invalid credentials）
    @allure.title("TC02 - 错误密码（预期全局 Invalid credentials）")
    def test_invalid_password(self):
        self.login_page.login("Admin", "wrongpass123")
        error = self.login_page.get_error_message()
        assert "Invalid credentials" in error, f"预期全局错误未出现，实际: {error}"
        assert not self.login_page.is_login_success()

    # TC03 - 空用户名
    @allure.title("TC03 - 空用户名")
    def test_empty_username(self):
        self.login_page.login("", "admin123")
        error = self.login_page.get_error_message()
        assert "Username is required" in error or "Required" in error, f"预期用户名必填提示未出现，实际: {error}"
        assert not self.login_page.is_login_success()

    # TC04 - 空密码
    @allure.title("TC04 - 空密码")
    def test_empty_password(self):
        self.login_page.login("Admin", "")
        error = self.login_page.get_error_message()
        assert "Password is required" in error or "Required" in error, f"预期密码必填提示未出现，实际: {error}"
        assert not self.login_page.is_login_success()

    # TC05 - 两者都空
    @allure.title("TC05 - 两者都空")
    def test_both_empty(self):
        self.login_page.login("", "")
        error = self.login_page.get_error_message()
        assert any(x in error for x in ["Username is required", "Password is required", "Required"]), \
            f"预期必填提示未出现，实际: {error}"
        assert not self.login_page.is_login_success()

    @allure.title("TC06 - 特殊字符用户名（负向 - 预期失败）")
    @allure.severity(allure.severity_level.NORMAL)
    def test_special_chars_username(self):
        self.login_page.login("Admin@!#$%", "admin123")
        error = self.login_page.get_error_message()
        assert "Invalid credentials" in error or not self.login_page.is_login_success(), \
            "特殊字符用户名不应登录成功"