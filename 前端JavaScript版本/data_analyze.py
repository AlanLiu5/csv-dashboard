import pandas as pd
import matplotlib
matplotlib.use("Agg")
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