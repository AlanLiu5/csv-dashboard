from unicodedata import category

from fastapi import FastAPI
from fastapi.responses import FileResponse, HTMLResponse
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import uuid
import io
from fastapi.responses import StreamingResponse

app = FastAPI()


def run_analysis(
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    # 1. 读数据
    df = pd.read_csv("../data/data.csv")
    total_rows = len(df)

    # 2. 最小清洗
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # 3. filter
    if city != "":
        df = df[df["city"] == city]

    after_filter = len(df)

    # 4. aggregate
    metric = metric.lower()

    if metric == "count":
        result = df.groupby(group_by).size()

    elif metric == "sum":
        result = df.groupby(group_by)[field].sum()

    elif metric == "mean":
        result = df.groupby(group_by)[field].mean()

    else:
        return {"error": "metric must be count, sum, or mean"}

    # 5. sort + topk
    result = result.sort_values(ascending=False)
    result = result.head(k)

    # 6. 转成统一格式
    output = []
    for key, val in result.items():
        if isinstance(val, float):
            value = float(val)
        else:
            value = int(val)

        output.append({
            "group": key,
            "value": value
        })

    # 7. insight
    insight_lines = []
    if len(output) > 0:
        insight_lines.append(f"{output[0]['group']} has the highest {metric}.")
    if len(output) >= 2:
        if output[1]["value"] != 0 and output[0]["value"] / output[1]["value"] >= 1.5:
            insight_lines.append(
                f"There is a clear gap between {output[0]['group']} and {output[1]['group']}."
            )
        else:
            insight_lines.append(
                f"{output[0]['group']} and {output[1]['group']} are relatively close."
            )
        insight_lines.append(f"{output[-1]['group']} has the lowest {metric}.")

    return {
        "summary": {
            "total_rows": total_rows,
            "after_filter": after_filter,
            "group_by": group_by,
            "metric": metric,
            "field": field if metric in ["sum", "mean"] else "",
            "city": city,
            "k": k
        },
        "results": output,
        "insight": insight_lines
    }


@app.get("/")
def root():
    return {"message": "hello"}


@app.get("/analyze")
def analyze(
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    return run_analysis(group_by, metric, field, city, k)


@app.get("/chart")
def chart(
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    analysis = run_analysis(group_by, metric, field, city, k)

    if "error" in analysis:
        return analysis

    labels = [item["group"] for item in analysis["results"]]
    values = [item["value"] for item in analysis["results"]]

    # 1. 画图
    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(f"Top {group_by} ({metric})")
    plt.xlabel(group_by)
    plt.ylabel(metric)
    plt.tight_layout()

    # 2. 写到内存（关键）
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    plt.close()
    buffer.seek(0)

    # 3. 返回图片流
    return StreamingResponse(buffer, media_type="image/png")


@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(
    group_by: str = "category",
    metric: str = "sum",
    field: str = "amount",
    city: str = "",
    k: int = 10
):
    chart_url = f"/chart?group_by={group_by}&metric={metric}&field={field}&city={city}&k={k}"

    return f"""
    <html>
        <head>
            <title>CSV Dashboard</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background: #f7f8fa;
                    margin: 0;
                    padding: 40px;
                    color: #222;
                }}
                .container {{
                    max-width: 1000px;
                    margin: 0 auto;
                }}
                .card {{
                    background: white;
                    border-radius: 16px;
                    padding: 24px;
                    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
                    margin-bottom: 24px;
                }}
                h1 {{
                    margin-top: 0;
                    font-size: 40px;
                }}
                h2 {{
                    margin-bottom: 16px;
                }}
                .meta {{
                    color: #555;
                    line-height: 1.8;
                    font-size: 16px;
                }}
                .chart {{
                    text-align: center;
                }}
                img {{
                    max-width: 100%;
                    border-radius: 12px;
                }}
                form {{
                    display: grid;
                    grid-template-columns: repeat(2, 1fr);
                    gap: 16px;
                }}
                label {{
                    display: block;
                    font-weight: bold;
                    margin-bottom: 6px;
                }}
                input, select {{
                    width: 100%;
                    padding: 10px;
                    border: 1px solid #ccc;
                    border-radius: 8px;
                    box-sizing: border-box;
                }}
                .full {{
                    grid-column: 1 / -1;
                }}
                button {{
                    padding: 12px 20px;
                    border: none;
                    border-radius: 10px;
                    background: #222;
                    color: white;
                    cursor: pointer;
                    font-size: 16px;
                }}
            </style>
        </head>

        <body>
            <div class="container">
                <div class="card">
                    <h1>📊 CSV Dashboard</h1>
                    <p>This is a simple dashboard powered by FastAPI + pandas + matplotlib.</p>
                </div>

                <div class="card">
                    <h2>Controls</h2>
                    <form action="/dashboard" method="get"> 
                        <div>
                            <label>group_by</label>
                            <input type="text" name="group_by" value="{group_by}">
                        </div>

                        <div>
                            <label>metric</label>
                            <select name="metric">
                                <option value="sum" {"selected" if metric == "sum" else ""}>sum</option>
                                <option value="mean" {"selected" if metric == "mean" else ""}>mean</option>
                                <option value="count" {"selected" if metric == "count" else ""}>count</option>
                            </select>
                        </div>

                        <div>
                            <label>field</label>
                            <input type="text" name="field" value="{field}">
                        </div>

                        <div>
                            <label>city</label>
                            <input type="text" name="city" value="{city}">
                        </div>

                        <div>
                            <label>k</label>
                            <input type="number" name="k" value="{k}">
                        </div>

                        <div class="full">
                            <button type="submit">Update Dashboard</button>
                        </div>
                    </form>
                </div>

                <div class="card">
                    <h2>Parameters</h2>
                    <div class="meta">
                        <div><b>group_by:</b> {group_by}</div>
                        <div><b>metric:</b> {metric}</div>
                        <div><b>field:</b> {field}</div>
                        <div><b>city:</b> {city}</div>
                        <div><b>k:</b> {k}</div>
                    </div>
                </div>

                <div class="card chart">
                    <h2>Chart</h2>
                    <img src="{chart_url}" alt="chart">
                </div>
            </div>
        </body>
    </html>
    """
