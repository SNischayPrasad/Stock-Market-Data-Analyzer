"""
data_loader.py
--------------
Step 1 of the pipeline: get stock price data.

Two sources are supported:
1. Yahoo Finance (online, free) through the `yfinance` library.
2. A local CSV file (offline fallback) - useful when there is no internet,
   Yahoo is rate-limiting you, or you want reproducible results.
"""

from pathlib import Path

import pandas as pd

from src.config import DATA_DIR

REQUIRED_COLUMNS = ["Open", "High", "Low", "Close", "Volume"]


def fetch_from_yfinance(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Download daily OHLCV data from Yahoo Finance.

    Returns an empty DataFrame if anything goes wrong, so the caller
    can fall back to a CSV file.
    """
    try:
        import yfinance as yf  # imported here so the project still runs without it
    except ImportError:
        print("[WARN] yfinance is not installed. Run: pip install yfinance")
        return pd.DataFrame()

    try:
        print(f"[INFO] Downloading {ticker} from Yahoo Finance ({start} -> {end}) ...")
        df = yf.download(ticker, start=start, end=end, auto_adjust=False, progress=False)
    except Exception as exc:  # network errors, rate limits, etc.
        print(f"[WARN] Yahoo Finance download failed: {exc}")
        return pd.DataFrame()

    if df is None or df.empty:
        print("[WARN] Yahoo Finance returned no data.")
        return pd.DataFrame()

    # Newer yfinance versions return MultiIndex columns like ('Close', 'AAPL').
    # Flatten them to simple names: 'Close'.
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)

    df.index.name = "Date"
    return df


def load_from_csv(csv_path: Path) -> pd.DataFrame:
    """Load stock data from a CSV file that has a 'Date' column."""
    csv_path = Path(csv_path)
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV file not found: {csv_path}")

    print(f"[INFO] Loading data from CSV: {csv_path.name}")
    df = pd.read_csv(csv_path, parse_dates=["Date"], index_col="Date")
    return df


def save_raw_data(df: pd.DataFrame, ticker: str) -> Path:
    """Cache downloaded data in data/ so the next run can work offline."""
    path = DATA_DIR / f"{ticker.upper()}_raw.csv"
    df.to_csv(path)
    print(f"[INFO] Raw data saved to data/{path.name}")
    return path


def get_stock_data(ticker: str, start: str, end: str,
                   csv_path: Path | None = None,
                   offline: bool = False) -> tuple[pd.DataFrame, str]:
    """Main entry point: returns (dataframe, source_description).

    Order of preference:
      1. An explicit CSV path given by the user (--csv).
      2. Yahoo Finance (unless --offline).
      3. A cached file data/<TICKER>_raw.csv from a previous run.
      4. The bundled sample file data/sample_stock_data.csv.
    """
    if csv_path:
        return load_from_csv(csv_path), f"CSV file ({Path(csv_path).name})"

    if not offline:
        df = fetch_from_yfinance(ticker, start, end)
        if not df.empty:
            save_raw_data(df, ticker)
            return df, "Yahoo Finance (yfinance)"

    cached = DATA_DIR / f"{ticker.upper()}_raw.csv"
    if cached.exists():
        print("[INFO] Falling back to cached CSV.")
        return load_from_csv(cached), f"Cached CSV ({cached.name})"

    sample = DATA_DIR / "sample_stock_data.csv"
    print("[INFO] Falling back to bundled sample dataset (synthetic data).")
    return load_from_csv(sample), "Bundled sample CSV (synthetic demo data)"
