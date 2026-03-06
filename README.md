🚀 OrangeHRM Selenium 测试框架
这是一个针对 OrangeHRM 开源 demo 站点的自动化 UI 测试框架，使用 Selenium、Pytest 和 Allure 报告构建。目前聚焦登录模块，并通过 GitHub Actions 实现 CI 集成。
 
📋 项目概述
项目名称
OrangeHRM Selenium Test Framework
简介
一个针对 OrangeHRM 开源 demo 站点的自动化 UI 测试框架，使用 Selenium + Pytest + Allure 构建。目前聚焦登录模块测试，并集成 GitHub Actions CI，支持自动化运行和报告生成。
核心功能

Page Object Model (POM)：组织化结构，提高维护性。
登录模块测试：覆盖正向场景（有效凭证）和负向场景（无效密码、空字段等）。
Allure 报告：详细测试报告，包括步骤、日志和失败截图。
GitHub Actions CI：push/PR 时自动测试，并生成 Allure 结果 artifact。
日志记录：自定义日志，便于调试。
未来计划：扩展到 PIM 模块（员工管理），支持 CRUD 测试。

 
🏗️ 整体架构
text测试触发层 (Pytest / GitHub Actions)
↓
Selenium 浏览器引擎 (Edge / Chrome)
↓
目标站点 (OrangeHRM Demo)
↓
结果处理层 (Pytest 断言 + Allure 附件)
↓
决策反馈层 (报告生成 + CI 状态)
↓
数据持久化层 (logs / reports)
↓
可视化层 (Allure 报告)
 
📁 项目结构
textOrangeHRM-Test-Framework/
├── config/               # 测试数据 (e.g., employee_data.yaml)
├── logs/                 # 日志文件
├── pages/                # 页面对象模型
│   ├── base_page.py
│   ├── login_page.py
│   └── pim_page.py       # (可选 PIM 模块)
├── reports/              # Allure 报告
├── tests/                # 测试用例
│   ├── test_login.py
│   └── test_pim.py       # (可选 PIM 测试)
├── utils/                # 工具如 logger
├── conftest.py           # Pytest  fixture
├── pytest.ini            # Pytest 配置
├── requirements.txt      # 依赖
├── .github/workflows/ci.yml  # GitHub Actions CI
└── README.md             # 本文档
 
🔧 环境搭建
前置条件

Python 3.11+
Microsoft Edge 浏览器 (本地测试)
推荐使用虚拟环境

一键部署

克隆仓库：textgit clone https://github.com/your-username/OrangeHRM-Test-Framework.git
cd OrangeHRM-Test-Framework
创建并激活虚拟环境：textpython -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
安装依赖：textpip install -r requirements.txt

 
🚀 运行测试

运行所有测试 (本地，使用 Edge)：textpytest tests/ -v -s
只运行登录模块：textpytest tests/test_login.py -v -s
生成 Allure 报告：textpytest tests/ -v --alluredir=reports/allure-results
allure serve reports/allure-results

 
🔄 GitHub Actions CI 集成

配置仓库 Settings → Actions → General → 启用 Workflow permissions（Read and write）。
push/PR 时自动触发测试 + Allure 结果 artifact。
查看 CI 状态：仓库 Actions 标签。

流水线自动运行测试。如果失败，下载 artifact 查看 Allure 结果。
 
📊 监控与报告

Allure 报告示例：运行测试后，浏览器打开详细报告，包括步骤、日志和失败截图。
在线报告 (如果部署到 GitHub Pages)：View Allure Report
报告示例：测试用例状态持续时间细节test_valid_credentialsPASSED10s成功登录 Dashboardtest_invalid_passwordFAILED8sInvalid credentials 提示
