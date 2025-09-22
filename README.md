# 自动化测试项目

本项目是基于 **Pytest + Allure** 搭建的自动化测试框架，支持 **接口测试** 与 **UI 测试**，实现测试用例参数化、日志记录、截图保存与可视化报告。

---

## 📂 项目结构

├── case_data/ # 测试数据文件（YAML/JSON/CSV）
├── conf/ # 配置文件（环境配置、账号信息）
├── lib/ # 公共库（API 封装、UI 基类、工具方法）
├── logs/ # 日志文件
├── report/
│ └── html/ # Allure 生成的测试报告
├── screenshots/ # UI 自动化失败截图
├── test_case/ # 测试用例目录
├── main_test.py # 启动入口
├── pytest.ini # Pytest 配置

---

## 🚀 功能特性
- **接口自动化**
  - YAML 参数化管理
  - Requests 封装 + 公共断言
- **UI 自动化**
  - Selenium 封装 PageObject 模式
  - 自动截图 + 日志记录
- **报告**
  - Allure 报告生成
  - 用例步骤可视化
- **日志**
  - 分 API/UI 类型日志存储
  - 支持调试、运行级别日志切换

---

## 🛠 环境依赖

- Python 3.8+
- pip 依赖：
  ```bash
  pip install -r requirements.txt

  
浏览器驱动（UI 自动化需要）

Chrome + ChromeDriver

Allure 命令行工具（报告查看）

安装 Allure
▶️ 运行方式
1. 运行所有用例
pytest main_test.py

2. 运行指定模块
pytest test_case/api/test_login.py -vs
pytest test_case/ui/test_home.py -vs

3. 生成 Allure 报告
# 运行用例并生成 allure-results
pytest --alluredir=report/allure-results

# 启动 Allure 报告服务
allure serve report/allure-results


📊 日志 & 截图

执行日志保存在 logs/ 下，按日期分类

UI 自动化失败时，会在 screenshots/ 保存截图

📌 目录约定

case_data/ → 管理测试数据，支持参数化

conf/ → 不同环境的配置文件（dev/test/prod）

lib/ → 公共库（driver 封装、api 请求、工具类）

test_case/ → 测试用例，按模块区分

✨ TODO

集成 CI/CD（Jenkins/GitLab）

丰富断言方式（数据库校验、MQ 校验）

接口 + UI 混合业务场景测试

4.报告内容：

![image](https://github.com/user-attachments/assets/2fa573b4-dee1-4f67-8b5c-36c505c802bb)

5.收集测试结果发送到企业微信：

![image](https://github.com/user-attachments/assets/c0e7d6d4-bf6f-4c8c-bcd5-2c3ac1357643)
