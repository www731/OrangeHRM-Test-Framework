# conftest.py （完整版，支持 Edge / Chrome 切换）
import pytest
import os
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from utils.logger import get_logger

logger = get_logger(__name__)

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="edge",
                     help="浏览器类型: edge (本地默认) 或 chrome (CI 默认)")

@pytest.fixture(scope="function")
def driver(request):
    browser = request.config.getoption("--browser").lower()
    # 或用环境变量覆盖（CI 时更方便）
    browser = os.getenv("BROWSER", browser)  # CI 可通过 env 设置

    driver_instance = None

    if browser == "edge":
        logger.info("启动 Edge 浏览器 (本地模式)")
        options = EdgeOptions()
        # 本地常用参数
        options.add_argument("--start-maximized")
        # options.add_argument("--headless=new")  # 本地调试时可注释
        # options.add_argument("--inprivate")

        service = EdgeService()  # Selenium 4 自动管理 msedgedriver
        driver_instance = webdriver.Edge(service=service, options=options)

    elif browser == "chrome":
        logger.info("启动 Chrome 浏览器 (CI / headless 模式)")
        options = ChromeOptions()
        # CI 必须加这些
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("--disable-gpu")

        service = ChromeService()  # Selenium 4 自动管理 chromedriver
        driver_instance = webdriver.Chrome(service=service, options=options)

    else:
        raise ValueError(f"不支持的浏览器: {browser}，只支持 edge 或 chrome")

    yield driver_instance

    try:
        driver_instance.quit()
        logger.info(f"{browser.upper()} 浏览器已关闭")
    except Exception as e:
        logger.warning(f"关闭浏览器出错: {e}")