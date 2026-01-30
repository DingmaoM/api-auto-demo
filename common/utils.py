import yaml
import random
import string
from datetime import datetime
from typing import Dict, Any
from config.config import Config
from config.logger_config import setup_logger
import pymysql


logger = setup_logger("utils")

connection = pymysql.connect(
        host='localhost',
        user='root',
        password='Lhzk0317@',
        database='linehope',
        charset='utf8mb4'
    )

def load_test_data(file_path: str = None) -> Dict[str, Any]:
    """加载YAML测试数据"""
    if file_path is None:
        file_path = Config.TEST_DATA_PATH

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.warning(f"测试数据文件未找到: {file_path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"YAML解析错误: {str(e)}")
        return {}


def generate_random_string(length: int = 10) -> str:
    """生成随机字符串"""
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))


def generate_random_email() -> str:
    """生成随机邮箱"""
    return f"{generate_random_string(8)}@example.com"


def generate_random_password(length=12):
    """生成随机密码（字母+数字）"""
    # 定义字符集：大写字母、小写字母、数字
    characters = string.digits
    # 随机选择字符生成密码
    password = ''.join(random.choice(characters) for _ in range(length))
    return password


def get_current_timestamp() -> str:
    """获取当前时间戳"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")


def select_data(table_name, row_name, conditions):
    """查询数据库数据"""
    try:
        with connection.cursor() as cursor:
            # sql = "SELECT {row_name} FROM {table_name} LIMIT 2"  # 查询结果的前两行
            # sql = "SELECT {row_name} FROM {table_name} ORDER BY ID ASC"  # 查询表结果根据ID升序排列
            sql = f"SELECT {row_name} FROM {table_name} {conditions}"  # 查询条件ID等于1的结果
            cursor.execute(sql)

            results = cursor.fetchall()
            return results
    finally:
        connection.close()


def add_data():
    """添加数据库数据"""
    try:
        with connection.cursor() as cursor:
            users_data = []
            for i in range(20):
                username = f"用户{i+1}"
                password = generate_random_password(10)
                users_data.append((username, password))
            sql = "INSERT INTO linehope.user (User, password) VALUES (%s, %s)"  # 查询条件ID等于1的结果
            respon = cursor.executemany(sql, users_data)
            connection.commit()
            return respon
    finally:
        connection.close()



if __name__ == '__main__':
    print(select_data("linehope.user", "User, password", "WHERE User = '用户2'"))
    # print(add_data())