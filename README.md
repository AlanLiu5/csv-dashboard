# CSV数据分析项目（CSV Dashboard）

这是一个从基础 Python 数据处理逐步升级到 Web 可视化的数据分析学习项目，适合初学者理解“数据分析 → API → 前端展示”的完整流程。

---

## 项目简介

本项目通过读取 CSV 数据，进行分组统计分析，并将结果通过网页可视化展示出来。

核心流程：

CSV数据 → 数据分析（pandas） → API（FastAPI） → 前端请求 → 图表展示（Chart.js）

---

## 项目结构

CSV数据分析/
├── data/                      # 原始 CSV 数据
├── 基础python版本/             # 纯 Python 数据处理
├── pandas版本/               # pandas 数据分析
├── sql版本/                  # SQL 思维分析
├── 前端JavaScript版本/        # Web 可视化版本（核心）
│   ├── static/               # 静态文件（CSS / JS）
│   │   ├── style.css
│   │   └── app.js
│   ├── templates/            # HTML 页面
│   │   └── dashboard.html
│   ├── data_analyze.py       # 数据分析逻辑
│   └── main.py               # FastAPI 后端入口
├── 自学api/                  # API 学习模块
└── README.md

---

## 功能说明

在前端页面中，用户可以：

- 输入 group_by（分组字段）
- 选择 metric（sum / mean / count）
- 设置筛选条件（如 city）
- 设置 Top K

系统会：

1. 调用后端 `/analyze` API
2. 返回 JSON 数据
3. 前端解析数据
4. 动态展示：
   - 数据结果（results）
   - 总结信息（summary）
   - 分析结论（insight）
   - 图表（柱状图）

---

## 技术栈

后端：
- FastAPI
- pandas

前端：
- HTML
- CSS
- JavaScript（fetch）
- Chart.js

---

## 如何运行

1. 进入前端版本目录：

cd 前端JavaScript版本

2. 安装依赖：

pip install fastapi uvicorn pandas matplotlib jinja2

3. 启动服务：

uvicorn main:app --reload

4. 打开浏览器：

http://127.0.0.1:8000/dashboard

---

## 项目特点

- 从基础数据处理逐步升级
- 前后端完整打通
- 结构清晰（analysis / API / frontend 分离）
- 适合初学者理解真实项目流程

---

## 后续扩展方向

- 支持上传 CSV 文件
- 多种图表类型（折线图 / 饼图）
- 接入数据库
- 用户系统
- 前端框架（React / Vue）
- 部署上线

---

## 总结

这是一个从“写数据分析代码”升级到“构建可视化数据产品”的完整实践项目，适合用来建立工程能力和项目经验。