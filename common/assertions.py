# import json
# from typing import Dict, Any, List, Union
# import allure
#
#
# class Assertions:
#     """断言工具类"""
#
#     @staticmethod
#     @allure.step("验证状态码")
#     def assert_status_code(response, expected_code: int):
#         """验证HTTP状态码"""
#         assert response.status_code == expected_code, \
#             f"状态码验证失败: 期望 {expected_code}, 实际 {response.status_code}"
#
#     @staticmethod
#     @allure.step("验证响应体包含字段")
#     def assert_json_contains(response_data: Dict, expected_data: Dict):
#         """验证响应体包含特定字段和值"""
#         for key, value in expected_data.items():
#             assert key in response_data, f"响应中缺少字段: {key}"
#             assert response_data[key] == value, \
#                 f"字段 {key} 的值不匹配: 期望 {value}, 实际 {response_data[key]}"
#
#     @staticmethod
#     @allure.step("验证响应时间")
#     def assert_response_time(response, max_time: float):
#         """验证响应时间不超过阈值"""
#         assert response.elapsed.total_seconds() <= max_time, \
#             f"响应时间超过阈值: {response.elapsed.total_seconds()} > {max_time}"
#
#     @staticmethod
#     @allure.step("验证JSON Schema")
#     def assert_json_schema(response_data: Dict, schema: Dict):
#         """验证JSON结构（简化的schema验证）"""
#
#         # 这里可以集成jsonschema库进行完整验证
#         def check_schema(data, schema_dict, path=""):
#             for key, expected_type in schema_dict.items():
#                 full_path = f"{path}.{key}" if path else key
#                 assert key in data, f"缺少字段: {full_path}"
#
#                 if isinstance(expected_type, dict):
#                     # 如果是嵌套字典，递归检查
#                     check_schema(data[key], expected_type, full_path)
#                 elif isinstance(expected_type, type):
#                     # 检查类型
#                     assert isinstance(data[key], expected_type), \
#                         f"字段 {full_path} 类型错误: 期望 {expected_type}, 实际 {type(data[key])}"
#
#         check_schema(response_data, schema)
#
#     @staticmethod
#     @allure.step("验证列表长度")
#     def assert_list_length(data_list: List, expected_length: int):
#         """验证列表长度"""
#         assert len(data_list) == expected_length, \
#             f"列表长度不匹配: 期望 {expected_length}, 实际 {len(data_list)}"