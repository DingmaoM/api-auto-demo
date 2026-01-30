import pytest
import allure
import random
import string
from faker import Faker
from data.test_data_loader import data_loader

fake = Faker()


class TestDynamicDataGeneration:
    """动态生成测试数据的测试"""

    @allure.story("动态数据生成")
    @allure.title("使用Faker生成测试数据")
    def test_with_faker_data(self, api_client):
        """使用Faker库动态生成测试数据"""

        # 生成随机用户数据
        test_cases = []
        for i in range(3):  # 生成3个测试用例
            test_case = {
                "test_name": f"创建随机用户{i + 1}",
                "method": "POST",
                "endpoint": "/users",
                "request": {
                    "name": fake.name(),
                    "email": fake.email(),
                    "gender": random.choice(["male", "female"]),
                    "status": random.choice(["active", "inactive"]),
                    "address": {
                        "street": fake.street_address(),
                        "city": fake.city(),
                        "zipcode": fake.zipcode()
                    }
                },
                "expected": {
                    "status_code": 201
                }
            }
            test_cases.append(test_case)

        # 执行所有生成的测试用例
        for test_case in test_cases:
            with allure.step(f"执行: {test_case['test_name']}"):
                success, response, resp_obj = api_client.post(
                    test_case['endpoint'],
                    data=test_case['request']
                )

                Assertions.assert_status_code(resp_obj, test_case['expected']['status_code'])

                # 验证响应包含生成的数据
                if success and response:
                    assert response['name'] == test_case['request']['name']
                    assert response['email'] == test_case['request']['email']

    @pytest.mark.parametrize("user_count", [1, 3, 5])
    @allure.story("批量用户创建")
    def test_batch_user_creation(self, api_client, user_count):
        """批量创建用户测试"""

        created_users = []

        for i in range(user_count):
            user_data = {
                "name": f"Batch User {i + 1}",
                "email": f"batch.user{i + 1}@example.com",
                "gender": "male",
                "status": "active"
            }

            with allure.step(f"创建用户 {i + 1}/{user_count}"):
                success, response, resp_obj = api_client.post("/users", data=user_data)

                Assertions.assert_status_code(resp_obj, 201)
                created_users.append(response.get('id'))

        # 验证创建的用户数
        with allure.step("验证批量创建结果"):
            success, all_users, _ = api_client.get("/users")
            assert len(all_users) >= user_count, \
                f"创建的用户数不足: 期望至少{user_count}，实际{len(all_users)}"

        # 清理：删除创建的用户
        with allure.step("清理测试数据"):
            for user_id in created_users:
                api_client.delete(f"/users/{user_id}")