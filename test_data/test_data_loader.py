import yaml
import os
import json
import csv
from typing import Dict, Any, List, Union
from config.logger_config import setup_logger

logger = setup_logger("data_loader")


class DataLoader:
    """数据加载器，支持多种格式的测试数据"""

    def __init__(self, data_dir: str = None):
        if data_dir is None:
            # 默认数据目录
            current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.data_dir = os.path.join(current_dir, "test_data")
        else:
            self.data_dir = data_dir

    def load_yaml(self, file_name: str) -> Union[Dict, List]:
        """加载YAML文件"""
        file_path = os.path.join(self.data_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = yaml.safe_load(file)
                logger.info(f"成功加载YAML文件: {file_name}")
                return data
        except FileNotFoundError:
            logger.error(f"YAML文件未找到: {file_path}")
            raise
        except yaml.YAMLError as e:
            logger.error(f"YAML解析错误: {str(e)}")
            raise

    def load_json(self, file_name: str) -> Union[Dict, List]:
        """加载JSON文件"""
        file_path = os.path.join(self.data_dir, file_name)
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"成功加载JSON文件: {file_name}")
                return data
        except FileNotFoundError:
            logger.error(f"JSON文件未找到: {file_path}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"JSON解析错误: {str(e)}")
            raise

    def load_csv(self, file_name: str) -> List[Dict]:
        """加载CSV文件"""
        file_path = os.path.join(self.data_dir, file_name)
        try:
            data = []
            with open(file_path, 'r', encoding='utf-8') as file:
                csv_reader = csv.DictReader(file)
                for row in csv_reader:
                    data.append(dict(row))
                logger.info(f"成功加载CSV文件: {file_name}, 共{len(data)}行数据")
            return data
        except FileNotFoundError:
            logger.error(f"CSV文件未找到: {file_path}")
            raise
        except Exception as e:
            logger.error(f"CSV加载错误: {str(e)}")
            raise

    def get_test_cases(self, file_name: str, test_suite: str = None) -> List[Dict]:
        """获取测试用例数据"""
        data = self.load_yaml(file_name)

        if test_suite:
            # 获取特定测试套件的数据
            return data.get(test_suite, [])

        # 返回所有测试数据
        test_cases = []
        for suite_name, cases in data.items():
            if isinstance(cases, list):
                test_cases.extend(cases)
        return test_cases

    def generate_test_data(self, template: Dict, data_list: List[Dict]) -> List[Dict]:
        """基于模板和数据列表生成测试数据"""
        test_data = []
        for data_item in data_list:
            # 深拷贝模板
            import copy
            test_item = copy.deepcopy(template)

            # 填充数据
            for key, value in data_item.items():
                # 支持嵌套键的替换，如: "user.name"
                if '.' in key:
                    keys = key.split('.')
                    temp = test_item
                    for k in keys[:-1]:
                        if k not in temp:
                            temp[k] = {}
                        temp = temp[k]
                    temp[keys[-1]] = value
                else:
                    test_item[key] = value

            test_data.append(test_item)

        return test_data


# 创建全局数据加载器实例
data_loader = DataLoader()
# data_d = data_loader.load_yaml("api_test_cases.yaml")
# data_r = data_loader.get_test_cases("api_test_cases.yaml", "auth_test_cases")
# data_loader.generate_test_data()
print(data_loader.generate_test_data())