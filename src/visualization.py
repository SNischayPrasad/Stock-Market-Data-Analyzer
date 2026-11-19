"""
visualization.py
----------------
Step 6 of the pipeline: charts. Every function saves a PNG into images/
and returns the file path, so the report can link to it.
"""

import matplotlib

matplotlib.use("Agg")  # draw to files, no pop-up windows (works on servers too)

import matplotlib.pyplot as plt
import seaborn as sns

from src.config import IMAGES_DIR, LONG_WINDOW, SHORT_WINDOW, TREND_WINDOW

sns.set_theme(style="whitegrid")
FIGSIZE = (12, 6)
DPI = 120


def _save(fig, name: str):
    path = IMAGES_DIR / name
    fig.tight_layout()
    fig.savefig(path, dpi=DPI)
    plt.close(fig)
    print(f"[CHART] Saved images/{path.name}")
    return path


def plot_closing_price(df, ticker):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(df.index, df["Close"], color="#1f77b4", linewidth=1.5, label="Close")
    hi, lo = df["Close"].idxmax(), df["Close"].idxmin()
    ax.scatter([hi], [df.loc[hi, "Close"]], color="green", zorder=5, label="Highest close")
    ax.scatter([lo], [df.loc[lo, "Close"]], color="red", zorder=5, label="Lowest close")
    ax.set_title(f"{ticker} - Closing Price")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    return _save(fig, f"{ticker}_closing_price.png")


def plot_moving_averages(df, ticker):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(df.index, df["Close"], label="Close", color="gray", alpha=0.6)
    ax.plot(df.index, df[f"SMA_{SHORT_WINDOW}"], label=f"SMA {SHORT_WINDOW}", color="#ff7f0e")
    ax.plot(df.index, df[f"SMA_{LONG_WINDOW}"], label=f"SMA {LONG_WINDOW}", color="#2ca02c")
    if df[f"SMA_{TREND_WINDOW}"].notna().any():
        ax.plot(df.index, df[f"SMA_{TREND_WINDOW}"], label=f"SMA {TREND_WINDOW}",
                color="#d62728", linestyle="--")

    golden = df[df["Signal"] > 0]
    death = df[df["Signal"] < 0]
    ax.scatter(golden.index, golden["Close"], marker="^", s=120, color="green",
               label="Golden cross", zorder=5)
    ax.scatter(death.index, death["Close"], marker="v", s=120, color="red",
               label="Death cross", zorder=5)
    ax.set_title(f"{ticker} - Moving Averages & Crossover Signals")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend(loc="upper left")
    return _save(fig, f"{ticker}_moving_averages.png")


def plot_daily_returns(df, ticker):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    r = df["Daily_Return"].dropna() * 100
    colors = ["green" if v >= 0 else "red" for v in r]
    ax.bar(r.index, r, color=colors, width=1.0)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{ticker} - Daily Returns (%)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Daily return (%)")
    return _save(fig, f"{ticker}_daily_returns.png")


def plot_return_distribution(df, ticker):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    r = df["Daily_Return"].dropna() * 100
    sns.histplot(r, bins=60, kde=True, ax=ax, color="#1f77b4")
    ax.axvline(r.mean(), color="green", linestyle="--", label=f"Mean {r.mean():.2f}%")
    ax.axvline(r.quantile(0.05), color="red", linestyle="--",
               label=f"5% VaR {r.quantile(0.05):.2f}%")
    ax.set_title(f"{ticker} - Distribution of Daily Returns")
    ax.set_xlabel("Daily return (%)")
    ax.legend()
    return _save(fig, f"{ticker}_return_distribution.png")


def plot_volatility(df, ticker):
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 8), sharex=True)
    ax1.plot(df.index, df["Rolling_Volatility"] * 100, color="purple")
    ax1.set_title(f"{ticker} - 20-Day Rolling Volatility (annualised %)")
    ax1.set_ylabel("Volatility (%)")
    ax2.fill_between(df.index, df["Drawdown"] * 100, 0, color="red", alpha=0.4)
    ax2.set_title(f"{ticker} - Drawdown from Peak (%)")
    ax2.set_ylabel("Drawdown (%)")
    ax2.set_xlabel("Date")
    return _save(fig, f"{ticker}_volatility_drawdown.png")


def plot_cumulative_return(df, ticker):
    fig, ax = plt.subplots(figsize=FIGSIZE)
    ax.plot(df.index, df["Cumulative_Return"] * 100, color="#17becf")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_title(f"{ticker} - Cumulative Return (%)")
    ax.set_xlabel("Date")
    ax.set_ylabel("Return since start (%)")
    return _save(fig, f"{ticker}_cumulative_return.png")


def plot_monthly_heatmap(monthly_table, ticker):
    fig, ax = plt.subplots(figsize=(12, max(3, len(monthly_table) * 1.0)))
    sns.heatmap(monthly_table * 100, annot=True, fmt=".1f", cmap="RdYlGn",
                center=0, ax=ax, cbar_kws={"label": "Return (%)"})
    ax.set_title(f"{ticker} - Monthly Returns (%)")
    return _save(fig, f"{ticker}_monthly_heatmap.png")


def create_all_charts(df, monthly_table, ticker):
    return [
        plot_closing_price(df, ticker),
        plot_moving_averages(df, ticker),
        plot_daily_returns(df, ticker),
        plot_return_distribution(df, ticker),
        plot_volatility(df, ticker),
        plot_cumulative_return(df, ticker),
        plot_monthly_heatmap(monthly_table, ticker),
    ]
