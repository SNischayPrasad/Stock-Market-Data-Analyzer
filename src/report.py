"""
report.py
---------
Step 7 of the pipeline: turn numbers into a human-readable report.

Produces:
  reports/<TICKER>_report.md   - Markdown report (renders nicely on GitHub)
  reports/<TICKER>_summary.csv - one-row table of metrics (for Excel / Power BI)
"""

import pandas as pd

from src.config import LONG_WINDOW, REPORTS_DIR, SHORT_WINDOW

DISCLAIMER = ("This report is generated for EDUCATIONAL PURPOSES ONLY. "
              "It is NOT financial or investment advice. Past performance does "
              "not guarantee future results.")


def pct(x: float) -> str:
    return f"{x * 100:.2f}%"


def generate_insights(s: dict) -> list[str]:
    """Rule-based plain-English insights from the summary numbers."""
    ins = []
    direction = "gained" if s["total_return"] >= 0 else "lost"
    ins.append(f"{s['ticker']} {direction} {pct(abs(s['total_return']))} over the period "
               f"({s['start_date']} to {s['end_date']}), a CAGR of {pct(s['cagr'])}.")
    ins.append(f"Current trend based on {SHORT_WINDOW}/{LONG_WINDOW}-day moving averages: "
               f"**{s['trend']}**.")
    ins.append(f"Annualised volatility is {pct(s['annual_volatility'])}, "
               f"which we classify as **{s['risk_level']}** risk.")
    ins.append(f"The deepest fall from a peak (max drawdown) was {pct(s['max_drawdown'])} "
               f"on {s['max_drawdown_date']}.")
    ins.append(f"On a typical bad day (95% VaR) the stock can drop about "
               f"{pct(abs(s['var_95']))} or more, which happens on ~5% of days.")
    ins.append(f"The stock closed higher on {pct(s['positive_days_pct'])} of trading days.")

    sr = s["sharpe_ratio"]
    if sr >= 1:
        quality = "good - returns have compensated well for the risk taken"
    elif sr >= 0:
        quality = "modest - returns only slightly beat the risk-free rate for the risk taken"
    else:
        quality = "poor - returns did not beat the risk-free rate"
    ins.append(f"Sharpe ratio of {sr:.2f} is {quality}.")
    ins.append(f"Last moving-average crossover signal: {s['last_signal']}.")
    return ins


def build_markdown(s: dict, cleaning_log: dict, source: str, chart_paths) -> str:
    lines = [
        f"# Stock Analysis Report: {s['ticker']}",
        "",
        f"> {DISCLAIMER}",
        "",
        f"**Data source:** {source}  ",
        f"**Period:** {s['start_date']} to {s['end_date']} ({s['trading_days']} trading days)",
        "",
        "## 1. Price Summary",
        "| Metric | Value |",
        "|---|---|",
        f"| First close | {s['first_close']:.2f} |",
        f"| Last close | {s['last_close']:.2f} |",
        f"| Highest price | {s['highest_price']:.2f} ({s['highest_date']}) |",
        f"| Lowest price | {s['lowest_price']:.2f} ({s['lowest_date']}) |",
        f"| Average close | {s['average_close']:.2f} |",
        f"| Average daily volume | {s['average_volume']:,.0f} |",
        "",
        "## 2. Return Analysis",
        "| Metric | Value |",
        "|---|---|",
        f"| Total return | {pct(s['total_return'])} |",
        f"| CAGR (annualised growth) | {pct(s['cagr'])} |",
        f"| Average daily return | {pct(s['avg_daily_return'])} |",
        f"| Best day | {pct(s['best_day'])} ({s['best_day_date']}) |",
        f"| Worst day | {pct(s['worst_day'])} ({s['worst_day_date']}) |",
        f"| Positive days | {pct(s['positive_days_pct'])} |",
        "",
        "## 3. Risk Summary",
        "| Metric | Value |",
        "|---|---|",
        f"| Daily volatility | {pct(s['daily_volatility'])} |",
        f"| Annualised volatility | {pct(s['annual_volatility'])} |",
        f"| Risk level | {s['risk_level']} |",
        f"| Sharpe ratio | {s['sharpe_ratio']:.2f} |",
        f"| Maximum drawdown | {pct(s['max_drawdown'])} ({s['max_drawdown_date']}) |",
        f"| 1-day 95% VaR | {pct(s['var_95'])} |",
        "",
        "## 4. Trend & Signals",
        f"- **Current trend:** {s['trend']}",
        f"- **Golden crosses:** {s['golden_crosses']}  |  **Death crosses:** {s['death_crosses']}",
        f"- **Last signal:** {s['last_signal']}",
        "",
        "## 5. Key Insights",
        *[f"- {i}" for i in generate_insights(s)],
        "",
        "## 6. Data Quality",
        f"- Rows loaded: {cleaning_log['rows_before']}, rows after cleaning: {cleaning_log['rows_after']}",
        f"- Duplicates removed: {cleaning_log['duplicates_removed']}, "
        f"missing values fixed: {cleaning_log['missing_values_found']}, "
        f"invalid rows removed: {cleaning_log['invalid_rows_removed']}",
        "",
        "## 7. Charts",
    ]
    for p in chart_paths:
        title = p.stem.replace(f"{s['ticker']}_", "").replace("_", " ").title()
        lines += [f"### {title}", f"![{title}](../images/{p.name})", ""]
    lines += ["---", f"*{DISCLAIMER}*", ""]
    return "\n".join(lines)


def save_reports(s: dict, cleaning_log: dict, source: str, chart_paths):
    md_path = REPORTS_DIR / f"{s['ticker']}_report.md"
    md_path.write_text(build_markdown(s, cleaning_log, source, chart_paths), encoding="utf-8")

    csv_path = REPORTS_DIR / f"{s['ticker']}_summary.csv"
    pd.DataFrame([s]).to_csv(csv_path, index=False)

    print(f"[REPORT] Saved reports/{md_path.name}")
    print(f"[REPORT] Saved reports/{csv_path.name}")
    return md_path, csv_path


def print_console_summary(s: dict) -> None:
    bar = "=" * 60
    print(f"\n{bar}\n  STOCK ANALYSIS SUMMARY: {s['ticker']}\n{bar}")
    rows = [
        ("Period", f"{s['start_date']} -> {s['end_date']} ({s['trading_days']} days)"),
        ("First / Last close", f"{s['first_close']:.2f} -> {s['last_close']:.2f}"),
        ("Highest price", f"{s['highest_price']:.2f} on {s['highest_date']}"),
        ("Lowest price", f"{s['lowest_price']:.2f} on {s['lowest_date']}"),
        ("Total return", pct(s["total_return"])),
        ("CAGR", pct(s["cagr"])),
        ("Annual volatility", f"{pct(s['annual_volatility'])} ({s['risk_level']} risk)"),
        ("Sharpe ratio", f"{s['sharpe_ratio']:.2f}"),
        ("Max drawdown", pct(s["max_drawdown"])),
        ("95% 1-day VaR", pct(s["var_95"])),
        ("Trend", s["trend"]),
        ("Last signal", s["last_signal"]),
    ]
    for k, v in rows:
        print(f"  {k:<20}: {v}")
    print(bar)
    print("  Key insights:")
    for i in generate_insights(s):
        print("   -", i.replace("**", ""))
    print(bar)
    print("  DISCLAIMER: Educational project - not financial advice.")
    print(bar + "\n")
