import csv
from collections import defaultdict
import matplotlib.pyplot as plt

def save_bar_chart(topk, title: str, output_file: str):
    """
    根据 topk 画柱状图并保存
    topk 形如:
    [('shopping', 135.0), ('food', 32.5), ('transport', 5.6)]
    """
    if not topk:
        return

    labels = [key for key, val in topk]
    values = [val for key, val in topk]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel("Category")
    plt.ylabel("Value")
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()

def read_rows(csv_filename: str):
    """读取CSV，返回每行一个dict（key是列名）"""
    rows = []
    with open(csv_filename, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(row)
    return rows

def group_count(rows, group_by: str):
    """按某列分组计数：返回 dict[group_value] = count"""
    counts = defaultdict(int)
    for r in rows:
        key = r.get(group_by, "")
        if key == "":
            continue
        counts[key] += 1
    return dict(counts)

def top_k_from_dict(d: dict, k: int):
    """通用TopK：按value降序，value相同按key升序"""
    return sorted(d.items(), key=lambda x: (-x[1], x[0]))[:k]

def format_topk(title: str, topk):
    lines = [title]
    for i, (key, val) in enumerate(topk, start=1):
        if isinstance(val, float):
            lines.append(f"{i}) {key} -> {val:.2f}")
        else:
            lines.append(f"{i}) {key} -> {val}")
    return "\n".join(lines)
def group_aggregate(rows, group_by: str, metric: str, field: str = ""):
    """
    metric:
      - "count": 每组行数
      - "sum":   每组 field 的和（field 必须是数字列）
      - "mean":  每组 field 的平均（field 必须是数字列）
    返回 dict[group_value] = 统计值
    """
    metric = metric.lower()

    # count 不需要 field
    if metric == "count":
        return group_count(rows, group_by)

    if field == "":
        raise ValueError("field is required for sum/mean")

    sums = defaultdict(float)
    counts = defaultdict(int)

    for r in rows:
        key = r.get(group_by, "")
        if key == "":
            continue

        raw = r.get(field, "")
        try:
            x = float(raw)
        except ValueError:
            # 非数字就跳过（鲁棒性）
            continue

        sums[key] += x
        counts[key] += 1

    if metric == "sum":
        return dict(sums)

    if metric == "mean":
        out = {}
        for key in sums:
            if counts[key] > 0:
                out[key] = sums[key] / counts[key]
        return out

    raise ValueError(f"unknown metric: {metric}")
def filter_rows(rows, filter_expr: str):
    """
    filter_expr 形如:
      city=Melbourne
      category=food

    返回筛选后的 rows
    """
    if filter_expr == "":
        return rows

    if "=" not in filter_expr:
        raise ValueError("filter must be like column=value")

    col, value = filter_expr.split("=", 1)

    out = []
    for r in rows:
        if r.get(col, "") == value:
            out.append(r)
    return out
def clean_rows(rows):
    """
    最小清洗 V1：
    - 对每个字符串字段做 strip()，去掉前后空格
    返回新的 rows
    """
    cleaned = []

    for r in rows:
        new_row = {}
        for key, value in r.items():
            if isinstance(value, str):
                new_row[key] = value.strip()
            else:
                new_row[key] = value
        cleaned.append(new_row)

    return cleaned
def generate_insight(topk, group_by: str, metric: str):
    """
    根据 topk 自动生成简单数据解释
    """
    if not topk:
        return "Insight:\n- No data available."

    lines = ["Insight:"]

    top1_key, top1_val = topk[0]
    lines.append(f"- {top1_key} has the highest {metric}.")

    if len(topk) >= 2:
        top2_key, top2_val = topk[1]
        if top2_val != 0 and top1_val / top2_val >= 1.5:
            lines.append(f"- There is a clear gap between {top1_key} and {top2_key}.")
        else:
            lines.append(f"- {top1_key} and {top2_key} are relatively close.")

    if len(topk) >= 2:
        last_key, last_val = topk[-1]
        lines.append(f"- {last_key} has the lowest {metric}.")

    return "\n".join(lines)