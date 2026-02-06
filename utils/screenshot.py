# utils/screenshot.py

import os
from datetime import datetime


def take_screenshot(driver, test_name: str) -> str:
    """
    拍摄当前浏览器截图，并保存到 reports/screenshots 文件夹
    返回截图文件的绝对路径
    """
    # 创建截图目录
    screenshots_dir = os.path.join("reports", "screenshots")
    os.makedirs(screenshots_dir, exist_ok=True)

    # 文件名：test_name_年月日_时分秒.png
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{test_name}_{timestamp}.png"
    filepath = os.path.join(screenshots_dir, filename)

    # 保存截图
    success = driver.save_screenshot(filepath)
    if success:
        print(f"截图已保存: {filepath}")  # 控制台可见
        return os.path.abspath(filepath)
    else:
        print("截图保存失败")
        return ""