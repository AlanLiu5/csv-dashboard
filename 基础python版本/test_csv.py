
from csv_lib import read_rows, clean_rows, filter_rows, group_aggregate


def test_read_rows():
    rows = read_rows("../data/data.csv")
    assert len(rows) == 7
    assert rows[0]["category"] == "food"
    assert rows[0]["city"] == "Melbourne"
def test_clean_rows():
    rows = [
        {"city": " Melbourne ", "amount": "12.5", "category": "food"},
        {"city": "Sydney", "amount": "8.0", "category": "food"}
    ]

    cleaned = clean_rows(rows)

    assert cleaned[0]["city"] == "Melbourne"
    assert cleaned[0]["amount"] == "12.5"
    assert cleaned[1]["city"] == "Sydney"


def test_dirty_sum():
    rows = read_rows("../data/dirty_data.csv")
    rows = clean_rows(rows)
    sums = group_aggregate(rows, "category", "sum", "amount")

    assert sums["food"] == 20.5
    assert sums["shopping"] == 135.0
    assert sums["transport"] == 12.0

def test_group_count():
    rows = read_rows("../data/data.csv")
    counts = group_aggregate(rows, "category", "count")
    assert counts["food"] == 3
    assert counts["shopping"] == 2
    assert counts["transport"] == 2


def test_group_sum():
    rows = read_rows("../data/data.csv")
    sums = group_aggregate(rows, "category", "sum", "amount")
    assert sums["food"] == 40.5
    assert sums["shopping"] == 135.0
    assert sums["transport"] == 17.6


def test_group_mean():
    rows = read_rows("../data/data.csv")
    means = group_aggregate(rows, "category", "mean", "amount")
    assert means["food"] == 13.5
    assert means["shopping"] == 67.5
    assert means["transport"] == 8.8


def test_filter_rows():
    rows = read_rows("../data/data.csv")
    mel_rows = filter_rows(rows, "city=Melbourne")

    assert len(mel_rows) == 5

    for r in mel_rows:
        assert r["city"] == "Melbourne"


def test_filter_and_sum():
    rows = read_rows("../data/data.csv")
    mel_rows = filter_rows(rows, "city=Melbourne")
    sums = group_aggregate(mel_rows, "category", "sum", "amount")

    assert sums["food"] == 32.5
    assert sums["shopping"] == 135.0
    assert sums["transport"] == 5.6


if __name__ == "__main__":
    test_read_rows()
    test_group_count()
    test_group_sum()
    test_group_mean()
    test_filter_rows()
    test_filter_and_sum()
    test_clean_rows()
    test_dirty_sum()
    print("all csv tests passed")