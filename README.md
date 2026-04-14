# CSV数据分析项目

这是一个从零构建的数据分析项目，围绕同一份 CSV 数据，分别用不同技术实现分析能力：

- 基础 Python
- pandas
- SQL (SQLite)
- FastAPI API

项目目标不是只做一个工具，而是理解：

👉 同一个数据问题，如何用不同工具实现  
👉 如何把分析能力升级为“可调用的服务”

---

## 项目结构

CSV数据分析/
├── data/
├── 基础python版本/
├── v2_pandas/
├── v3_sql/
└── 自学api/

---

## 数据分析流程

CSV → 清洗 → filter → group by → sum / mean / count → topK → 输出（summary / insight / chart）

---

## 各版本说明

### 基础 Python
手写实现数据处理逻辑

### pandas
用 DataFrame 做数据分析

### SQL
用 SQLite + SQL 查询实现分析

### API
用 FastAPI 封装分析能力

---

## 快速开始（API）

cd 自学api  
uvicorn main:app --reload  

打开：
http://127.0.0.1:8000/docs

示例：
http://127.0.0.1:8000/analyze?group_by=category&metric=sum&field=amount&city=Melbourne&k=3

---

## 技术栈

Python / pandas / SQL / FastAPI / matplotlib

---

## 学习重点

- 数据分析流程
- pandas vs SQL
- CLI → API
- 参数驱动分析