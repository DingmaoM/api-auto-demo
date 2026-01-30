# API自动化测试框架

基于Python和pytest的接口自动化测试框架，使用Allure生成测试报告,集成数据库读写，断言类工具，日志模块，以及yaml数据驱动

## 功能特性

- ✅ 支持RESTful API测试
- ✅ 多种断言方式
- ✅ 测试数据管理
- ✅ HTML和Allure报告
- ✅ 并行测试执行
- ✅ 日志记录
- ✅ 配置文件管理
- ✅ 参数化测试
- ✅ 测试标记和筛选

## 安装依赖

```bash
pip install -r requirements.txt
```
## 项目结构
```bash
api-test-framework/
├── config/
│   ├── __init__.py
│   ├── config.py          # 配置文件
│   └── logger_config.py   # 日志配置
├── common/
│   ├── __init__.py
│   ├── api_client.py      # HTTP请求封装
│   ├── assertions.py      # 断言工具
│   └── utils.py          # 通用工具
├── tests/
│   ├── __init__.py
│   ├── conftest.py       # pytest配置和fixture
│   ├── test_user_api.py  # 用户相关测试用例
│   └── test_product_api.py # 产品相关测试用例
├── data/
│   └── test_data.yaml    # 测试数据
├── reports/              # 测试报告目录
├── logs/                 # 日志目录
├── requirements.txt      # 依赖包
├── pytest.ini           # pytest配置文件
└── README.md           # 项目说明
```

## 安装依赖
- pytest==7.4.0
- requests==2.31.0
- PyYAML==6.0.1
- allure-pytest==2.13.0
- pytest-html==4.1.1
- pytest-xdist==3.5.0
- pytest-ordering==0.6
- pytest-rerunfailures==13.0
- pytest-timeout==2.2.0
- Faker==20.0.1

## 记录
2026/1/16
yaml数据获取

@pytest.fixture是一个装饰器，用于定义测试夹具（test fixture）。测试夹具是一种函数，它可以在测试函数运行之前和/或之后执行一些代码，为测试提供数据和上下文环境，也可以用来进行清理工作。

主要用途：
- 准备测试数据：例如创建数据库记录、读取文件等。
- 设置测试环境：例如启动服务器、建立数据库连接等。
- 清理工作：例如删除临时文件、关闭连接等。

通过scope参数，可以指定夹具的作用域。作用域决定了夹具在何时被创建和销毁。

function（默认）：每个测试函数都会运行一次夹具。

class：每个测试类运行一次夹具。

module：每个模块运行一次夹具。

package：每个包运行一次夹具。

session：整个测试会话运行一次夹具。

