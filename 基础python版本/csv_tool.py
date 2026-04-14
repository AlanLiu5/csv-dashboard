import argparse
from csv_lib import (read_rows, clean_rows, filter_rows, group_aggregate,
                     top_k_from_dict, format_topk, generate_insight,
                     save_bar_chart)
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True, help="csv file name")
    parser.add_argument("--group-by", required=True, help="column to group by")
    parser.add_argument("--metric", default="count", help="count|sum|mean (default=count)")
    parser.add_argument("--field", default="", help="numeric field for sum/mean (e.g., amount)")
    parser.add_argument("--k", type=int, default=10, help="top k (default=10)")
    parser.add_argument("--output", default="", help="output report file (optional)")
    parser.add_argument("--filter", default="", help="filter like city=Melbourne")
    parser.add_argument("--chart", action="store_true", help="save bar chart")
    args = parser.parse_args()

    if args.k <= 0:
        print("k must be a positive integer")
        return

    rows = read_rows(args.input)
    total_rows = len(rows)
    rows = clean_rows(rows)
    try:
        rows = filter_rows(rows, args.filter)
    except ValueError as e:
        print(e)
        return
    after_filter = len(rows)
    try:
        counts = group_aggregate(rows, args.group_by, args.metric, args.field)
    except ValueError as e:
        print(e)
        return
    topk = top_k_from_dict(counts, args.k)
    insight = generate_insight(topk, args.group_by, args.metric)
    summary_lines = [
        "Summary:",
        f"- total_rows: {total_rows}",
        f"- after_filter: {after_filter}",
        f"- group_by: {args.group_by}",
        f"- metric: {args.metric}",
    ]

    main_report = format_topk(f"Top {args.group_by} ({args.metric}):", topk)
    report = "\n".join(summary_lines) + "\n\n" + main_report + "\n\n" + insight
    print(report)
    if args.chart:
        chart_file = "chart.png"
        save_bar_chart(topk, f"Top {args.group_by} ({args.metric})", chart_file)
        print(f"Chart saved to {chart_file}")

    if args.output != "":
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report + "\n")
        print(f"Saved to {args.output}")



if __name__ == "__main__":
    main()