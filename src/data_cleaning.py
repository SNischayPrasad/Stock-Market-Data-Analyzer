"""
data_cleaning.py
----------------
Step 2 of the pipeline: make raw data trustworthy before analysing it.

Real-world data is messy: missing rows, duplicated dates, text instead of
numbers, wrong sort order. Garbage in = garbage out, so we clean first.
"""

import pandas as pd

from src.data_loader import REQUIRED_COLUMNS


def clean_stock_data(df: pd.DataFrame) -> tuple[pd.DataFrame, dict]:
    """Clean a raw OHLCV DataFrame.

    Returns the cleaned DataFrame and a small dict describing what was fixed
    (handy for the report and for explaining your work in interviews).
    """
    log = {"rows_before": len(df)}
    df = df.copy()

    # 1. Keep only the columns we need (plus 'Adj Close' if present)
    keep = [c for c in REQUIRED_COLUMNS + ["Adj Close"] if c in df.columns]
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Data is missing required columns: {sorted(missing)}")
    df = df[keep]

    # 2. Make sure the index is a proper DatetimeIndex, sorted oldest -> newest
    df.index = pd.to_datetime(df.index, errors="coerce")
    df = df[~df.index.isna()]
    df = df.sort_index()

    # 3. Remove duplicate dates (keep the last record for that day)
    dupes = int(df.index.duplicated().sum())
    df = df[~df.index.duplicated(keep="last")]
    log["duplicates_removed"] = dupes

    # 4. Convert every column to numbers; bad text becomes NaN
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    # 5. Handle missing values
    log["missing_values_found"] = int(df.isna().sum().sum())
    # Forward-fill prices (carry the last known price forward - standard in finance)
    df = df.ffill()
    # Any NaN left at the very start can't be forward-filled -> drop those rows
    df = df.dropna()

    # 6. Remove impossible values (prices must be > 0, volume >= 0)
    bad = (df[["Open", "High", "Low", "Close"]] <= 0).any(axis=1) | (df["Volume"] < 0)
    log["invalid_rows_removed"] = int(bad.sum())
    df = df[~bad]

    log["rows_after"] = len(df)
    df.index.name = "Date"
    return df, log


def print_cleaning_log(log: dict) -> None:
    print("[INFO] Data cleaning summary:")
    print(f"       Rows before cleaning : {log['rows_before']}")
    print(f"       Duplicates removed   : {log['duplicates_removed']}")
    print(f"       Missing values fixed : {log['missing_values_found']}")
    print(f"       Invalid rows removed : {log['invalid_rows_removed']}")
    print(f"       Rows after cleaning  : {log['rows_after']}")
