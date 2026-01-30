import pytest
import allure
from common.assertions import Assertions


@allure.epic("产品管理")
@allure.feature("产品API")
class TestProductAPI:

    @allure.story("创建产品")
    @allure.title("创建新产品")
    def test_create_product(self, api_client, test_data_fixture):
        """测试创建产品"""
        product_data = test_data_fixture["product"]["create"]["valid_data"]

        success, response, resp_obj = api_client.post(
            "/products",
            data=product_data
        )

        Assertions.assert_status_code(resp_obj, 201)
        Assertions.assert_json_schema(response, {
            "id": int,
            "title": str,
            "price": (int, float),
            "description": str,
            "category": str
        })