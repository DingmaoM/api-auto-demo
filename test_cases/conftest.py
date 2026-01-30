import pytest
import allure
import os
from typing import Generator
from config.config import Config
from common.api_client import APIClient
from common.utils import load_test_data
from test_data.test_data_loader import data_loader

# 加载测试数据
test_data = load_test_data()


@pytest.fixture(scope="session")  # 整个测试会话运行一次夹具。
def api_client() -> Generator[APIClient, None, None]:
    """API客户端fixture"""
    client = APIClient(Config.BASE_URL)
    yield client
    client.session.close()


@pytest.fixture(scope="session")
def test_data_fixture() -> dict:
    """测试数据fixture"""
    return test_data


@pytest.fixture
def setup_teardown():
    """测试前后的setup/teardown"""
    # 测试前执行
    print("\n=== 测试开始 ===")
    yield
    # 测试后执行
    print("\n=== 测试结束 ===")


@pytest.fixture
def create_test_user(api_client):
    """创建测试用户并返回用户ID"""
    user_data = test_data["user"]["create"]["valid_data"]["name"]
    success, response, _ = api_client.post("/users", data=user_data)

    if success:
        user_id = response.get("id")
        yield user_id

        # 测试完成后清理数据
        api_client.delete(f"/users/{user_id}")
    else:
        yield None


# Hook函数，用于Allure环境信息
def pytest_configure(config):
    """pytest配置钩子"""
    # 创建Allure结果目录
    if not os.path.exists(Config.ALLURE_RESULTS_DIR):
        os.makedirs(Config.ALLURE_RESULTS_DIR)

    # 环境变量
    os.environ["ALLURE_RESULTS_DIR"] = Config.ALLURE_RESULTS_DIR


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """获取测试结果"""
    outcome = yield
    rep = outcome.get_result()

    # 添加失败截图（如果是Web测试）
    if rep.when == "call" and rep.failed:
        # 这里可以添加失败时的截图逻辑
        pass


def pytest_generate_tests(metafunc):
    """pytest参数化钩子，用于动态生成测试用例"""
    if "test_case_data" in metafunc.fixturenames:
        # 从YAML文件加载测试用例数据
        test_cases = []
        test_ids = []

        # 检查是否指定了测试套件
        if hasattr(metafunc.function, 'test_suite'):
            test_suite = metafunc.function.test_suite
            test_cases = data_loader.get_test_cases("api_test_cases.yaml", test_suite)
        else:
            # 默认加载所有测试用例
            test_cases = data_loader.get_test_cases("api_test_cases.yaml")

        # 为每个测试用例生成唯一的测试ID
        for case in test_cases:
            test_id = case.get('test_id', 'unknown')
            test_name = case.get('test_name', 'Unnamed Test')
            test_ids.append(f"{test_id}: {test_name}")

        # 参数化测试
        metafunc.parametrize("test_case_data", test_cases, ids=test_ids)


@pytest.fixture
def dynamic_test_case(test_case_data):
    """动态测试用例fixture"""
    # 这里可以对测试用例数据进行预处理
    test_case_data['_executed'] = False
    return test_case_data


# 自定义装饰器，用于标记使用数据驱动的测试
def data_driven(test_suite: str):
    """数据驱动测试装饰器"""
    def decorator(func):
        func.test_suite = test_suite
        return func
    return decorator