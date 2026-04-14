import argparse
import pandas as pd
import matplotlib.pyplot as plt

def save_bar_chart(topk, title: str, output_file: str, x_label: str, y_label: str):
    if not topk:
        return

    labels = [key for key, val in topk]
    values = [val for key, val in topk]

    plt.figure(figsize=(8, 5))
    plt.bar(labels, values)
    plt.title(title)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.tight_layout()
    plt.savefig(output_file)
    plt.close()
def generate_insight(topk, metric: str):
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
def format_topk(title: str, topk):
    lines = [title]
    for i, (key, val) in enumerate(topk, start=1):
        if isinstance(val, float):
            lines.append(f"{i}) {key} -> {val:.2f}")
        else:
            lines.append(f"{i}) {key} -> {val}")
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--chart", action="store_true", help="save bar chart")
    parser.add_argument("--input", required=True, help="csv file path")
    parser.add_argument("--group-by", required=True, help="column to group by")
    parser.add_argument("--metric", default="count", help="count|sum|mean")
    parser.add_argument("--field", default="", help="numeric field for sum/mean")
    parser.add_argument("--filter", default="", help="filter like city=Melbourne")
    parser.add_argument("--k", type=int, default=10, help="top k")
    args = parser.parse_args()

    if args.k <= 0:
        print("k must be a positive integer")
        return

    # 1. read csv
    df = pd.read_csv(args.input)
    total_rows = len(df)

    # 2. 最小清洗：字符串列去前后空格
    for col in df.columns:
        if df[col].dtype == "object":
            df[col] = df[col].astype(str).str.strip()

    # 3. filter
    if args.filter != "":
        if "=" not in args.filter:
            print("filter must be like column=value")
            return

        col, value = args.filter.split("=", 1)
        df = df[df[col] == value]

    after_filter = len(df)

    # 4. aggregate
    metric = args.metric.lower()

    if metric == "count":
        result = df.groupby(args.group_by).size()

    elif metric == "sum":
        if args.field == "":
            print("field is required for sum")
            return
        result = df.groupby(args.group_by)[args.field].sum()

    elif metric == "mean":
        if args.field == "":
            print("field is required for mean")
            return
        result = df.groupby(args.group_by)[args.field].mean()

    else:
        print("metric must be count, sum, or mean")
        return

    # 5. sort + topk
    result = result.sort_values(ascending=False)
    topk = list(result.head(args.k).items())
    insight = generate_insight(topk, args.metric)

    # 6. summary
    summary_lines = [
        "Summary:",
        f"- total_rows: {total_rows}",
        f"- after_filter: {after_filter}",
        f"- group_by: {args.group_by}",
        f"- metric: {args.metric}",
    ]
    if args.field != "":
        summary_lines.append(f"- field: {args.field}")

    # 7. report
    main_report = format_topk(f"Top {args.group_by} ({args.metric}):", topk)
    report = "\n".join(summary_lines) + "\n\n" + main_report + "\n\n" + insight

    print(report)
    if args.chart:
        chart_file = "chart.png"
        save_bar_chart(
            topk,
            f"Top {args.group_by} ({args.metric})",
            chart_file,
            args.group_by,
            args.metric
        )
        print(f"Chart saved to {chart_file}")


if __name__ == "__main__":
    main()