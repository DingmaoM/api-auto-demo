import os
from typing import Dict, Any


class Config:
    """项目配置"""

    # 基础配置
    BASE_URL = os.getenv("API_BASE_URL", "https://jsonplaceholder.typicode.com")

    # 测试数据路径
    TEST_DATA_PATH = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "test_data",
        "test_data.yaml"
    )

    # 超时设置
    TIMEOUT = 30

    # 重试配置
    RETRY_TIMES = 3
    RETRY_INTERVAL = 2

    # 日志配置
    LOG_LEVEL = "INFO"
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

    # Allure配置
    ALLURE_RESULTS_DIR = "./reports/allure-results"
    ALLURE_REPORT_DIR = "./reports/allure-report"

    # 测试数据
    TEST_DATA: Dict[str, Any] = {}