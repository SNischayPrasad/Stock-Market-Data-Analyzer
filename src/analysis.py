"""
analysis.py
-----------
Steps 3-5 of the pipeline: turn clean prices into insight.

  * Daily & cumulative returns  -> how much did the stock make/lose?
  * Moving averages (SMA)       -> what is the trend?
  * Volatility & drawdown       -> how risky is it?
  * Summary statistics          -> one dictionary used by the report
"""

import numpy as np
import pandas as pd

from src.config import (LONG_WINDOW, RISK_FREE_RATE, SHORT_WINDOW,
                        TRADING_DAYS, TREND_WINDOW, VOLATILITY_WINDOW)


# ---------------------------------------------------------------------------
# Feature engineering: add new columns to the price table
# ---------------------------------------------------------------------------
def add_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Daily return = (today's close / yesterday's close) - 1."""
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change()
    # Cumulative return = what Rs.1 invested on day 1 would have grown to, minus 1
    df["Cumulative_Return"] = (1 + df["Daily_Return"]).cumprod() - 1
    # Log returns are additive over time - preferred in quantitative finance
    df["Log_Return"] = np.log(df["Close"] / df["Close"].shift(1))
    return df


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """Simple Moving Average = average close of the last N days."""
    df = df.copy()
    df[f"SMA_{SHORT_WINDOW}"] = df["Close"].rolling(SHORT_WINDOW).mean()
    df[f"SMA_{LONG_WINDOW}"] = df["Close"].rolling(LONG_WINDOW).mean()
    df[f"SMA_{TREND_WINDOW}"] = df["Close"].rolling(TREND_WINDOW).mean()
    # Exponential MA reacts faster because recent days get more weight
    df[f"EMA_{SHORT_WINDOW}"] = df["Close"].ewm(span=SHORT_WINDOW, adjust=False).mean()
    return df


def add_volatility(df: pd.DataFrame) -> pd.DataFrame:
    """Rolling volatility = std-dev of daily returns, annualised."""
    df = df.copy()
    df["Rolling_Volatility"] = (
        df["Daily_Return"].rolling(VOLATILITY_WINDOW).std() * np.sqrt(TRADING_DAYS)
    )
    # Drawdown = % fall from the highest price seen so far
    running_max = df["Close"].cummax()
    df["Drawdown"] = df["Close"] / running_max - 1
    return df


def add_signals(df: pd.DataFrame) -> pd.DataFrame:
    """Golden cross / death cross signals from the short & long SMA.

    Golden cross: short SMA crosses ABOVE long SMA  -> bullish signal
    Death cross : short SMA crosses BELOW long SMA  -> bearish signal
    """
    df = df.copy()
    short, long_ = df[f"SMA_{SHORT_WINDOW}"], df[f"SMA_{LONG_WINDOW}"]
    above = (short > long_).astype(int)
    df["Signal"] = above.diff().fillna(0)   # +1 = golden cross, -1 = death cross
    df.loc[long_.isna(), "Signal"] = 0
    return df


def run_full_analysis(df: pd.DataFrame) -> pd.DataFrame:
    """Apply every feature step in order."""
    df = add_returns(df)
    df = add_moving_averages(df)
    df = add_volatility(df)
    df = add_signals(df)
    return df


# ---------------------------------------------------------------------------
# Summary metrics
# ---------------------------------------------------------------------------
def identify_trend(df: pd.DataFrame) -> str:
    """Classify the current trend using price vs moving averages."""
    last = df.iloc[-1]
    s, l = last[f"SMA_{SHORT_WINDOW}"], last[f"SMA_{LONG_WINDOW}"]
    price = last["Close"]
    if pd.isna(s) or pd.isna(l):
        return "Not enough data"
    if price > s > l:
        return "Strong Uptrend"
    if price < s < l:
        return "Strong Downtrend"
    if s > l:
        return "Uptrend (weakening)" if price < s else "Uptrend"
    return "Downtrend (recovering)" if price > s else "Downtrend"


def risk_level(annual_vol: float) -> str:
    """Rough, rule-of-thumb label for annualised volatility."""
    if annual_vol < 0.15:
        return "Low"
    if annual_vol < 0.30:
        return "Moderate"
    if annual_vol < 0.50:
        return "High"
    return "Very High"


def compute_summary(df: pd.DataFrame, ticker: str) -> dict:
    """Return all headline numbers in one dictionary."""
    returns = df["Daily_Return"].dropna()
    first_close, last_close = df["Close"].iloc[0], df["Close"].iloc[-1]
    n_days = len(df)
    years = n_days / TRADING_DAYS

    total_return = last_close / first_close - 1
    cagr = (1 + total_return) ** (1 / years) - 1 if years > 0 else np.nan
    annual_vol = returns.std() * np.sqrt(TRADING_DAYS)
    annual_ret = returns.mean() * TRADING_DAYS
    sharpe = (annual_ret - RISK_FREE_RATE) / annual_vol if annual_vol else np.nan
    # 95% one-day historical Value at Risk: the loss we exceed only 5% of days
    var_95 = returns.quantile(0.05)

    signals = df[df["Signal"] != 0]
    last_signal = "None"
    if not signals.empty:
        s = signals.iloc[-1]
        kind = "Golden Cross (bullish)" if s["Signal"] > 0 else "Death Cross (bearish)"
        last_signal = f"{kind} on {signals.index[-1].date()}"

    return {
        "ticker": ticker.upper(),
        "start_date": df.index[0].date(),
        "end_date": df.index[-1].date(),
        "trading_days": n_days,
        "first_close": first_close,
        "last_close": last_close,
        "highest_price": df["High"].max(),
        "highest_date": df["High"].idxmax().date(),
        "lowest_price": df["Low"].min(),
        "lowest_date": df["Low"].idxmin().date(),
        "average_close": df["Close"].mean(),
        "average_volume": df["Volume"].mean(),
        "total_return": total_return,
        "cagr": cagr,
        "avg_daily_return": returns.mean(),
        "best_day": returns.max(),
        "best_day_date": returns.idxmax().date(),
        "worst_day": returns.min(),
        "worst_day_date": returns.idxmin().date(),
        "positive_days_pct": (returns > 0).mean(),
        "daily_volatility": returns.std(),
        "annual_volatility": annual_vol,
        "risk_level": risk_level(annual_vol),
        "sharpe_ratio": sharpe,
        "max_drawdown": df["Drawdown"].min(),
        "max_drawdown_date": df["Drawdown"].idxmin().date(),
        "var_95": var_95,
        "trend": identify_trend(df),
        "golden_crosses": int((df["Signal"] > 0).sum()),
        "death_crosses": int((df["Signal"] < 0).sum()),
        "last_signal": last_signal,
    }


def monthly_returns(df: pd.DataFrame) -> pd.DataFrame:
    """Month-by-month returns table (rows = year, columns = month)."""
    monthly = df["Close"].resample("ME").last().pct_change().dropna()
    table = pd.DataFrame({
        "Year": monthly.index.year,
        "Month": monthly.index.strftime("%b"),
        "Return": monthly.values,
    })
    order = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    pivot = table.pivot(index="Year", columns="Month", values="Return")
    return pivot.reindex(columns=[m for m in order if m in pivot.columns])
