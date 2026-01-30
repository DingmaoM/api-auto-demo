import logging
import os
from datetime import datetime
from config.config import Config


def setup_logger(name: str = "api_test") -> logging.Logger:
    """配置日志记录器"""

    # 创建日志目录
    log_dir = "./logs"
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # 生成日志文件名（按天）
    log_file = os.path.join(
        log_dir,
        f"api_test_{datetime.now().strftime('%Y%m%d')}.log"
    )

    # 创建logger
    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, Config.LOG_LEVEL))

    # 避免重复添加handler
    if not logger.handlers:
        # 文件处理器
        file_handler = logging.FileHandler(log_file, encoding='utf-8')
        file_handler.setLevel(logging.DEBUG)

        # 控制台处理器
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)

        # 格式化器
        formatter = logging.Formatter(Config.LOG_FORMAT)
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加处理器
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    return logger