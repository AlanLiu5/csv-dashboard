import argparse
import pandas as pd
import sqlite3


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--group-by", required=True)
    parser.add_argument("--metric", default="count")
    parser.add_argument("--field", default="")
    parser.add_argument("--filter", default="")
    parser.add_argument("--k", type=int, default=10)

    args = parser.parse_args()

    # 1. CSV -> DB
    df = pd.read_csv(args.input)
    total_rows = len(df)

    conn = sqlite3.connect("data.db")
    df.to_sql("transactions", conn, if_exists="replace", index=False)

    # 2. after_filter 行数（单独查一次）
    after_filter = total_rows
    if args.filter:
        col, value = args.filter.split("=", 1)
        count_query = f"""
        SELECT COUNT(*)
        FROM transactions
        WHERE {col} = '{value}';
        """
        cursor = conn.cursor()
        cursor.execute(count_query)
        after_filter = cursor.fetchone()[0]

    # 3. 构造 SELECT / ORDER
    metric = args.metric.lower()

    if metric == "count":
        select_part = f"{args.group_by}, COUNT(*)"
        order_part = "COUNT(*)"

    elif metric == "sum":
        if args.field == "":
            print("field is required for sum")
            conn.close()
            return
        select_part = f"{args.group_by}, SUM({args.field})"
        order_part = f"SUM({args.field})"

    elif metric == "mean":
        if args.field == "":
            print("field is required for mean")
            conn.close()
            return
        select_part = f"{args.group_by}, AVG({args.field})"
        order_part = f"AVG({args.field})"

    else:
        print("metric must be count, sum, or mean")
        conn.close()
        return

    # 4. 构造 WHERE
    where_part = ""
    if args.filter:
        col, value = args.filter.split("=", 1)
        where_part = f"WHERE {col} = '{value}'"

    # 5. 拼 SQL
    query = f"""
    SELECT {select_part}
    FROM transactions
    {where_part}
    GROUP BY {args.group_by}
    ORDER BY {order_part} DESC
    LIMIT {args.k};
    """

    # 6. 执行
    cursor = conn.cursor()
    cursor.execute(query)
    results = cursor.fetchall()

    # 7. Summary
    print("Summary:")
    print(f"- total_rows: {total_rows}")
    print(f"- after_filter: {after_filter}")
    print(f"- group_by: {args.group_by}")
    print(f"- metric: {args.metric}")
    if args.field != "":
        print(f"- field: {args.field}")

    print("\nResults:")
    for row in results:
        print(row)

    conn.close()


if __name__ == "__main__":
    main()