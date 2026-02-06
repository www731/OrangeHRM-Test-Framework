# conftest.py
import pytest
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from utils.logger import get_logger

logger = get_logger(__name__)

@pytest.fixture(scope="function")
def driver():
    """使用 Selenium 4 内置的自动管理 EdgeDriver 方式"""
    options = Options()
    options.add_argument("--start-maximized")      # 启动时最大化窗口
    # options.add_argument("--headless=new")       # 如果想无头模式，取消注释
    # options.add_argument("--inprivate")          # 可选：隐私模式
    # options.add_argument("--disable-dev-shm-usage")
    # options.add_argument("--no-sandbox")

    service = Service()  # ← 关键：Selenium 4 会自动找/下载匹配的 msedgedriver

    driver_instance = webdriver.Edge(service=service, options=options)
    logger.info("Edge 浏览器启动成功")

    yield driver_instance

    try:
        driver_instance.quit()
        logger.info("Edge 浏览器已关闭")
    except Exception as e:
        logger.warning(f"关闭浏览器时出错: {e}")