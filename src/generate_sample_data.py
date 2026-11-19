"""
generate_sample_data.py
-----------------------
Creates data/sample_stock_data.csv - a SYNTHETIC (fake) stock price series
so the project runs even with no internet.

It uses Geometric Brownian Motion, the same random-walk model behind the
Black-Scholes option pricing formula. A fixed random seed makes the file
identical every time.

Run:  python -m src.generate_sample_data
"""

import numpy as np
import pandas as pd

from src.config import DATA_DIR, ensure_folders


def generate(start="2023-01-02", days=500, start_price=150.0,
             annual_drift=0.12, annual_vol=0.25, seed=42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    dates = pd.bdate_range(start=start, periods=days)  # business days only
    dt = 1 / 252
    shocks = rng.normal((annual_drift - 0.5 * annual_vol ** 2) * dt,
                        annual_vol * np.sqrt(dt), days)
    close = start_price * np.exp(np.cumsum(shocks))

    open_ = np.r_[start_price, close[:-1]] * (1 + rng.normal(0, 0.003, days))
    high = np.maximum(open_, close) * (1 + np.abs(rng.normal(0, 0.006, days)))
    low = np.minimum(open_, close) * (1 - np.abs(rng.normal(0, 0.006, days)))
    volume = rng.integers(40_000_000, 90_000_000, days)

    df = pd.DataFrame({"Open": open_, "High": high, "Low": low,
                       "Close": close, "Adj Close": close, "Volume": volume}).round(2)
    df.insert(0, "Date", dates)

    # Inject a little "dirty data" so the cleaning step has something to fix
    df.loc[10, "Close"] = np.nan                       # missing value
    df.loc[25, "Volume"] = np.nan                      # missing value
    df = pd.concat([df, df.iloc[[50]]]).sort_values("Date")  # duplicate row
    return df


if __name__ == "__main__":
    ensure_folders()
    out = DATA_DIR / "sample_stock_data.csv"
    generate().to_csv(out, index=False)
    print(f"Sample data written to {out}")
