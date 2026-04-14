# FastAPI 数据分析接口

将 pandas 数据分析逻辑封装为 API。

---

## 启动

uvicorn main:app --reload

---

## 接口

### GET /
测试接口

---

### GET /analyze

参数：

- group_by
- metric (sum / mean / count)
- field
- city
- k

---

## 示例

http://127.0.0.1:8000/analyze?group_by=category&metric=sum&field=amount&city=Melbourne&k=3

---

## 返回

- summary
- results
- insight

---

## 文档

http://127.0.0.1:8000/docs

---

## 核心

API = 路由 + 参数 + pandas + JSON