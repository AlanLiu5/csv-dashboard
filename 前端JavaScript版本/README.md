# 前端JavaScript版本

这是一个基于 **FastAPI + pandas + HTML/CSS/JavaScript + Chart.js** 搭建的 CSV 数据分析可视化项目。

项目目标是：  
后端负责读取 CSV、分析数据并返回 JSON；前端负责通过 `fetch()` 获取数据，并将分析结果和图表动态展示在网页上。

---

## 项目功能

本项目目前支持：

- 读取本地 CSV 数据
- 按指定字段进行分组分析（如 `category`）
- 支持三种统计方式：
  - `sum`
  - `mean`
  - `count`
- 支持按 `city` 过滤数据
- 支持设置 `top k`
- 返回分析结果 JSON
- 前端动态显示：
  - 参数信息
  - summary（摘要）
  - insight（分析结论）
  - results（结果列表）
  - 柱状图（Chart.js）

---

## 技术栈

### 后端
- FastAPI
- pandas
- matplotlib（早期版本用于后端画图）
- Jinja2Templates

### 前端
- HTML
- CSS
- JavaScript
- Chart.js

---

## 项目结构

前端JavaScript版本/
├── static/
│   ├── style.css          # 页面样式
│   └── app.js             # 前端交互逻辑
├── templates/
│   └── dashboard.html     # 页面模板
├── data_analyze.py        # 数据分析逻辑
├── main.py                # FastAPI 应用入口
└── README.md              # 项目说明

---

## 主要路由说明

### `/`
基础测试接口，用于确认服务启动成功。

### `/analyze`
分析接口，返回 JSON 数据。

支持参数：
- `group_by`
- `metric`
- `field`
- `city`
- `k`

返回内容主要包括：
- `summary`
- `results`
- `insight`

### `/dashboard`
返回前端页面模板 `dashboard.html`。

### `/static/...`
提供静态资源访问：
- `style.css`
- `app.js`

---

## 项目运行逻辑

### 1. 后端分析
`main.py` 接收请求后，调用 `data_analyze.py` 中的 `run_analysis()`：

- 读取 CSV
- 清洗字符串字段
- 根据参数过滤
- 分组统计
- 排序取 Top K
- 生成 summary / results / insight

### 2. 前端请求数据
浏览器打开 `/dashboard` 后：

- 加载 HTML 模板
- 加载 `style.css`
- 加载 `app.js`

在 `app.js` 中，前端通过：

```javascript
fetch("/analyze?...")

向后端请求 JSON 数据。

### 3. 前端展示结果
前端拿到 JSON 后：

- 把 summary 显示到页面
- 把 insight 显示到页面
- 把 results 显示为文本列表
- 把 results 拆成 `labels` 和 `values`
- 使用 Chart.js 绘制柱状图

---

## 当前版本特点

这个版本和前面只用 Python / pandas 的版本相比，最大的升级是：

- 不再只是命令行输出
- 不再只是后端直接返回图片
- 开始形成“前后端分工”的项目结构

当前版本实现的是：

- 后端返回 JSON
- 前端自己画图

这更接近现代 Web 项目的基本模式。

---

## 我在这个版本中学到的内容

通过这个版本，我主要练习了以下能力：

### 后端部分
- FastAPI 基本路由编写
- API 参数接收
- JSON 返回
- 模板页面返回
- 静态文件挂载（`/static`）

### 前端部分
- HTML 页面结构搭建
- CSS 页面样式拆分
- JavaScript 基础语法
- `fetch()` 请求后端 API
- `document.getElementById()` 获取页面元素
- `innerHTML` / `textContent` 更新页面内容
- `forEach()` 遍历数组
- 使用 Chart.js 进行前端绘图

### 项目结构部分
- 将分析逻辑拆分到独立文件
- 将 HTML / CSS / JS 分离
- 使用 `templates/` 与 `static/` 组织项目

---

## 后续可以继续升级的方向

这个项目后面还可以继续扩展，例如：

- 支持更多图表类型（折线图、饼图）
- 支持上传 CSV 文件
- 支持更多筛选条件
- 支持下载分析结果
- 把更多路由进一步拆分
- 增加数据库支持
- 增加用户系统或登录功能
- 优化页面 UI/UX

---

## 运行方式

### 1. 安装依赖
建议先创建虚拟环境，然后安装依赖：

```bash
pip install fastapi uvicorn pandas matplotlib jinja2

### 2. 启动项目

```bash
uvicorn main:app --reload

### 3. 浏览器访问

```text
http://127.0.0.1:8000/dashboard

---

## 总结

这是一个从“基础数据分析”走向“前后端结合可视化”的过渡版本项目。

它的意义不只是做出一个页面，而是让我真正理解了：

- 后端如何提供数据
- 前端如何请求数据
- JSON 如何驱动页面和图表
- 一个小型 Web 项目应该如何组织结构

这个版本已经不再只是练习语法，而是一个完整的小型数据分析可视化项目原型。