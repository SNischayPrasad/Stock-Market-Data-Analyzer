"""
main.py - Stock Market Data Analyzer
====================================
Runs the full pipeline:

  collect data -> clean -> returns -> moving averages -> volatility
  -> charts -> report

Examples
--------
    python main.py                                   # AAPL, default dates
    python main.py --ticker MSFT --start 2022-01-01 --end 2024-12-31
    python main.py --ticker RELIANCE.NS              # Indian stock (NSE)
    python main.py --csv data/sample_stock_data.csv --ticker DEMO
    python main.py --offline                         # never touch the internet

DISCLAIMER: Educational project. Not financial advice.
"""

import argparse
import sys

from src import config
from src.analysis import compute_summary, monthly_returns, run_full_analysis
from src.data_cleaning import clean_stock_data, print_cleaning_log
from src.data_loader import get_stock_data
from src.report import print_console_summary, save_reports
from src.visualization import create_all_charts


def parse_args():
    p = argparse.ArgumentParser(description="Stock Market Data Analyzer")
    p.add_argument("--ticker", default=config.DEFAULT_TICKER,
                   help="Ticker symbol, e.g. AAPL, MSFT, TCS.NS (default: AAPL)")
    p.add_argument("--start", default=config.DEFAULT_START, help="Start date YYYY-MM-DD")
    p.add_argument("--end", default=config.DEFAULT_END, help="End date YYYY-MM-DD")
    p.add_argument("--csv", default=None, help="Path to a local CSV instead of downloading")
    p.add_argument("--offline", action="store_true",
                   help="Skip Yahoo Finance and use cached/sample CSV")
    return p.parse_args()


def main():
    args = parse_args()
    ticker = args.ticker.upper()
    config.ensure_folders()

    print("\n=== Stock Market Data Analyzer ===\n")

    # 1. Collect
    raw, source = get_stock_data(ticker, args.start, args.end,
                                 csv_path=args.csv, offline=args.offline)
    if raw.empty:
        sys.exit("[ERROR] No data available. Check the ticker or provide --csv.")
    print(f"[INFO] Source: {source} | {len(raw)} rows loaded")
    if source.startswith("Bundled sample"):
        # Never label synthetic data with a real company's name
        print(f"[WARN] No real data for {ticker}; analysing synthetic sample as 'DEMO'.")
        ticker = "DEMO"

    # 2. Clean
    df, cleaning_log = clean_stock_data(raw)
    print_cleaning_log(cleaning_log)
    print("\n[INFO] Data preview (first 5 rows):")
    print(df.head().round(2).to_string())

    # 3-5. Analyse
    df = run_full_analysis(df)
    summary = compute_summary(df, ticker)
    monthly = monthly_returns(df)

    processed_path = config.OUTPUTS_DIR / f"{ticker}_processed.csv"
    df.to_csv(processed_path)
    monthly.to_csv(config.OUTPUTS_DIR / f"{ticker}_monthly_returns.csv")
    print(f"\n[INFO] Processed data saved to outputs/{processed_path.name}")

    # 6. Visualise
    charts = create_all_charts(df, monthly, ticker)

    # 7. Report
    save_reports(summary, cleaning_log, source, charts)
    print_console_summary(summary)


if __name__ == "__main__":
    main()
