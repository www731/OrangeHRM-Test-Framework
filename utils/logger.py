# utils/logger.py
import logging
from logging.handlers import RotatingFileHandler
import os

# 日志文件存放路径（项目根目录下的 logs 文件夹）
LOG_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "logs")
os.makedirs(LOG_DIR, exist_ok=True)  # 如果 logs 文件夹不存在，就自动创建

LOG_FILE = os.path.join(LOG_DIR, "test.log")


def get_logger(name: str) -> logging.Logger:
    """
    获取一个命名的 logger
    每个模块/类用自己的名字作为 logger name，便于区分谁在输出日志

    用法示例：
    self.logger = get_logger(__name__)          # 在类里用
    # 或
    logger = get_logger("test_login")           # 在测试文件里用
    """
    logger = logging.getLogger(name)

    # 防止重复添加 handler（多次调用 get_logger 也不会重复写日志）
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)  # 默认记录 INFO 及以上级别（INFO, WARNING, ERROR, CRITICAL）

    # 控制台输出（开发时看得到）
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # 文件输出 - 旋转：最大 10MB，保留 5 个备份文件
    file_handler = RotatingFileHandler(
        LOG_FILE,
        maxBytes=10 * 1024 * 1024,  # 10MB
        backupCount=5,  # 保留 test.log.1 ~ test.log.5
        encoding='utf-8'
    )
    file_handler.setLevel(logging.INFO)

    # 日志格式：时间 - logger名字 - 级别 - 消息
    formatter = logging.Formatter(
        '%(asctime)s | %(name)-20s | %(levelname)-8s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger