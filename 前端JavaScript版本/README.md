# 📊 CSV Dashboard

A simple web dashboard built with **FastAPI + pandas + JavaScript + Chart.js**.

It reads a CSV file, performs analysis, and displays results dynamically on a web page.

---

## 🚀 Features

- 📂 Read and analyze CSV data
- 🔍 Group by different fields (e.g., category)
- 📊 Support metrics: sum / mean / count
- 🎯 Filter by city
- 📈 Display results as:
  - Text summary
  - Insights
  - Bar chart (Chart.js)
- ⚡ Frontend fetches JSON from backend (modern web pattern)

---

## 🧱 Project Structure
CSV数据分析/
├── static/             # Frontend assets
│   ├── style.css
│   └── app.js
├── templates/          # HTML templates
│   └── dashboard.html
├── data/               # CSV data
│   └── data.csv
├── data_analyze.py     # Data processing logic
├── main.py             # FastAPI app entry
└── README.md

