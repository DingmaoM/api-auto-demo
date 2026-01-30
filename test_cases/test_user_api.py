import pytest
import allure
# from common.assertions import Assertions
from common.utils import load_test_data
from common.utils import select_data

# 加载测试数据
test_data = load_test_data()


@allure.epic("用户管理")
@allure.feature("用户API")
class TestUserAPI:

    # @allure.story("创建用户")
    # @allure.title("创建有效用户 - 成功")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_create_user_success(self, api_client, test_data_fixture):
    #     """测试创建有效用户"""
    #     user_data = test_data_fixture["user"]["create"]["valid_data"]
    #
    #     with allure.step("发送创建用户请求"):
    #         success, response, resp_obj = api_client.post("/users", data=user_data)
    #
    #     with allure.step("验证响应"):
    #         Assertions.assert_status_code(resp_obj, 201)
    #         Assertions.assert_json_contains(response, {
    #             "name": user_data["name"],
    #             "email": user_data["email"]
    #         })

    @allure.story("获取用户")
    @allure.title("获取用户列表 - 成功")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_users_success(self, api_client):
        """测试获取用户列表"""
        success, response, resp_obj = api_client.get("/users/1")
        user_data = test_data["user"]["create"]["valid_data"]["name"]
        assert user_data == response["name"]  # 获取接口数据字典中name和yaml数据中name对比

        # Assertions.assert_status_code(resp_obj, 200)
        # Assertions.assert_list_length(response, 10)  # 假设返回10个用户

    @allure.story("获取城市")
    @allure.title("获取城市 - 成功")
    @allure.severity(allure.severity_level.NORMAL)
    def test_get_citry(self, api_client):
        response = select_data("ID = 1")
        assert response[0][0] == "Kabul"


    # @allure.story("更新用户")
    # @allure.title("更新用户信息 - 成功")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_update_user_success(self, api_client, create_test_user):
    #     """测试更新用户信息"""
    #     user_id = create_test_user
    #     if not user_id:
    #         pytest.skip("创建用户失败，跳过测试")
    #
    #     update_data = {
    #         "name": "Updated Name",
    #         "email": "updated@example.com"
    #     }
    #
    #     success, response, resp_obj = api_client.put(
    #         f"/users/{user_id}",
    #         data=update_data
    #     )
    #
    #     Assertions.assert_status_code(resp_obj, 200)
    #     Assertions.assert_json_contains(response, update_data)

    # @allure.story("删除用户")
    # @allure.title("删除用户 - 成功")
    # @allure.severity(allure.severity_level.CRITICAL)
    # def test_delete_user_success(self, api_client, create_test_user):
    #     """测试删除用户"""
    #     user_id = create_test_user
    #     if not user_id:
    #         pytest.skip("创建用户失败，跳过测试")
    #
    #     success, _, resp_obj = api_client.delete(f"/users/{user_id}")
    #     Assertions.assert_status_code(resp_obj, 204)
    #
    # @allure.story("创建用户")
    # @allure.title("创建无效用户 - 失败")
    # @allure.severity(allure.severity_level.NORMAL)
    # @pytest.mark.parametrize("invalid_data", [
    #     {"name": "", "email": "test@example.com"},
    #     {"name": "Test", "email": "invalid-email"},
    # ])
    # def test_create_user_invalid_data(self, api_client, invalid_data):
    #     """测试使用无效数据创建用户"""
    #     success, response, resp_obj = api_client.post("/users", data=invalid_data)
    #
    #     # 假设API会返回400状态码
    #     Assertions.assert_status_code(resp_obj, 400)


@pytest.mark.slow
@allure.story("性能测试")
class TestUserPerformance:

    @allure.title("批量获取用户性能测试")
    def test_bulk_get_users_performance(self, api_client):
        """性能测试：批量获取用户"""
        success, response, resp_obj = api_client.get("/users")
        print(resp_obj)
        # Assertions.assert_response_time(resp_obj, 2.0)  # 响应时间不超过2秒