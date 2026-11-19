# Stock Market Data Analyzer – Complete Project Guide

> ⚠️ Educational project. **Not financial advice.**

Contents
1. Project explanation · 2. Tech stack options · 3. Architecture · 4. Implementation plan · 5. Folder structure · 6. Installation · 7. Code walkthrough · 8. Virtual simulation · 9. How to run · 10. GitHub upload · 11. Proof-building plan (6 days) · 12. Screenshots checklist

---

## 1. Project Explanation

### What is a Stock Market Data Analyzer?
**Simple:** A program that looks at a company's past share prices and tells you, in numbers and charts, *how much it went up or down, which direction it's heading, and how risky the ride was*.

**Technical:** A Python data pipeline that ingests daily OHLCV (Open, High, Low, Close, Volume) time-series data, validates and cleans it, engineers features (returns, rolling moving averages, rolling volatility, drawdown, crossover signals), computes summary statistics (CAGR, annualised volatility, Sharpe ratio, maximum drawdown, historical VaR), and renders visualizations plus an automated Markdown/CSV report.

### What problem does it solve?
- Looking at a chart is subjective; this makes analysis **objective and repeatable**.
- Manual Excel analysis per stock is slow; this runs **any ticker in seconds**.
- Beginners don't know which metrics matter; the report turns numbers into **plain-English insights**.

### Why is it useful?
| User | Value |
|---|---|
| Investors | See long-term growth (CAGR) vs. the risk (volatility, drawdown) they'd have endured |
| Analysts | Standardised metrics to compare stocks in research notes |
| Traders | Moving-average trend and crossover signals |
| Finance/risk teams | Volatility & VaR for risk monitoring and limits |

### How companies use stock data analysis
- **Investment research:** analysts at funds/brokerages (e.g. Goldman Sachs, Motilal Oswal) compute returns and risk before recommending a stock.
- **Market tracking:** FinTech apps show 52-week high/low, % change and charts – exactly the numbers this project computes.
- **Trend analysis:** the 50-day and 200-day moving averages are watched on every trading desk; a "golden cross" makes financial news headlines.
- **Decision-making:** risk teams set position limits from volatility and Value-at-Risk.

### How Python analyses price movement
pandas stores prices as a time-indexed table. One-line operations do the heavy lifting:
`pct_change()` → returns, `rolling(50).mean()` → moving average, `rolling(20).std()` → volatility, `cummax()` → drawdown. Matplotlib/Seaborn turn those columns into charts, and simple rules turn metrics into sentences.

### Workflow
```
Stock data collection → Data cleaning → Price trend analysis → Moving averages
→ Returns calculation → Risk analysis → Visualization → Report generation
```

---

## 2. Tech Stack Options

| | Option A – Easy | Option B – Intermediate ✅ | Option C – Advanced |
|---|---|---|---|
| Tools | Python, pandas, Matplotlib, a CSV from Yahoo/NSE website | Python, pandas, NumPy, Matplotlib, Seaborn, yfinance, argparse, modular `src/` package, Markdown report | B + Plotly, Streamlit dashboard, SQL database, RSI/MACD, backtesting, pytest, GitHub Actions, cloud deployment |
| Difficulty | ⭐ Beginner | ⭐⭐ Beginner–Intermediate | ⭐⭐⭐ Intermediate–Advanced |
| Output | One script, 2–3 charts | CLI tool, 7 charts, processed CSVs, auto report | Interactive web app, strategy backtests, CI |

**Selected: Option B, with the optional Streamlit dashboard from Option C** – it's achievable in a week, shows clean software structure (what recruiters look for), and the dashboard adds a "wow" factor without being mandatory.

---

## 3. Project Architecture

```
┌──────────────────────── INPUT ────────────────────────┐
│  Ticker (AAPL, TCS.NS)   Date range   Optional CSV    │
└───────────────────────────┬───────────────────────────┘
                            ▼
┌──────────────── data_loader.py ───────────────────────┐
│ 1. --csv given?      → load CSV                        │
│ 2. yfinance download → cache to data/<T>_raw.csv       │
│ 3. download failed?  → cached CSV → sample CSV         │
└───────────────────────────┬───────────────────────────┘
                            ▼
┌──────────────── data_cleaning.py ─────────────────────┐
│ select cols · parse dates · sort · drop duplicates    │
│ to numeric · forward-fill NaN · remove price <= 0     │
└───────────────────────────┬───────────────────────────┘
                            ▼
┌──────────────── analysis.py ──────────────────────────┐
│ Daily/Cumulative/Log returns                          │
│ SMA 20/50/200, EMA 20 → trend label, cross signals    │
│ Rolling volatility, drawdown                          │
│ Summary: CAGR, Sharpe, max DD, VaR, high/low          │
└──────────────┬─────────────────────────┬──────────────┘
               ▼                         ▼
┌──── visualization.py ────┐  ┌──────── report.py ─────────┐
│ 7 PNG charts → images/   │  │ insights → reports/*.md    │
└──────────────────────────┘  │ metrics  → reports/*.csv   │
                              │ console summary            │
                              └────────────────────────────┘
         outputs/<T>_processed.csv  (every calculated column)
         dashboard.py reuses the same modules interactively
```

**Data flow:** a single pandas DataFrame travels through the pipeline. Each stage *adds columns* to it (it never mutates the original – every function works on `df.copy()`), so you can inspect the table after any step. `main.py` only orchestrates; logic lives in `src/`, which is why the dashboard can reuse it without duplication.

---

## 4. Implementation Plan

| Phase | What to do | Why | Expected output | Common beginner mistakes |
|---|---|---|---|---|
| 1. Setup | Install Python 3.10+, VS Code, Git; create a venv | Isolated, reproducible environment | `python --version` works, venv active | Installing packages globally; forgetting to activate venv |
| 2. Folders | Create the structure in §5, `requirements.txt`, `.gitignore` | Professional, navigable repo | Empty skeleton | Everything in one giant script; committing `venv/` |
| 3. Data collection | `data_loader.py` – yfinance + CSV fallback | Real data, but never blocked by network | `data/AAPL_raw.csv` | Not handling empty downloads; MultiIndex columns from new yfinance |
| 4. Cleaning | `data_cleaning.py` | Wrong data → wrong conclusions | Cleaning log printed | Dropping all NaN rows instead of forward-filling; unsorted dates |
| 5. EDA | Notebook: `head`, `info`, `describe`, first plots | Understand data before modelling | Notebook with outputs | Skipping EDA; not checking date range |
| 6. Moving averages | SMA 20/50/200, EMA, crossover signals | Identify trend | New SMA columns | Confusing calendar days with trading days; first N rows are NaN – that's normal |
| 7. Returns & volatility | `pct_change`, CAGR, rolling std × √252, drawdown, Sharpe, VaR | Quantify performance and risk | Summary dict | Annualising with 365 instead of 252; forgetting `dropna()` |
| 8. Visualization | 7 charts saved as PNG | Communicate insights | `images/*.png` | Not labelling axes; using `plt.show()` and never saving |
| 9. Report | Markdown + CSV + console summary | Decision-ready output | `reports/*` | Hard-coding numbers instead of computing them |
| 10. GitHub | README, screenshots, push | Proof of work | Public repo | One giant "final" commit; no README images |

---

## 5. Folder Structure

| Folder/File | Purpose |
|---|---|
| `data/` | Input data. `sample_stock_data.csv` (synthetic, committed) + downloaded `*_raw.csv` (git-ignored) |
| `notebooks/` | Jupyter notebook for exploration and screenshots |
| `src/` | Reusable Python modules – one per pipeline step |
| `outputs/` | Processed CSVs with every calculated column and monthly returns |
| `images/` | Saved PNG charts (used in README) |
| `reports/` | Generated Markdown report and summary CSV |
| `docs/` | This guide and interview prep |
| `README.md` | Front page of the GitHub repo |
| `requirements.txt` | Libraries to install |
| `.gitignore` | Files Git should not track (venv, cache) |
| `main.py` | Entry point – runs the full pipeline from the terminal |
| `dashboard.py` | Optional Streamlit web dashboard |

---

## 6. Installation Guide

1. **Install Python 3.10+** from <https://www.python.org/downloads/>. On Windows tick **"Add Python to PATH"**.
2. **Install Git** from <https://git-scm.com/>.
3. **Create a virtual environment and install libraries:**

**Windows (PowerShell):**
```powershell
cd Stock-Market-Data-Analyzer
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```
If activation is blocked: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` (run once).

**Mac / Linux:**
```bash
cd Stock-Market-Data-Analyzer
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

**Libraries:** pandas (tables), numpy (maths), matplotlib & seaborn (charts), yfinance (Yahoo data), plotly & streamlit (dashboard), jupyter (notebook).

---

## 7. Code Walkthrough
All code is in the repo – each file is commented line by line.

| File | Key functions |
|---|---|
| `src/config.py` | Paths, `SHORT_WINDOW=20`, `LONG_WINDOW=50`, `TREND_WINDOW=200`, `TRADING_DAYS=252`, `RISK_FREE_RATE=0.04` |
| `src/data_loader.py` | `fetch_from_yfinance()`, `load_from_csv()`, `get_stock_data()` (fallback chain) |
| `src/data_cleaning.py` | `clean_stock_data()` returns cleaned df + log |
| `src/analysis.py` | `add_returns()`, `add_moving_averages()`, `add_volatility()`, `add_signals()`, `compute_summary()`, `identify_trend()`, `monthly_returns()` |
| `src/visualization.py` | 7 `plot_*()` functions, `create_all_charts()` |
| `src/report.py` | `generate_insights()`, `save_reports()`, `print_console_summary()` |
| `src/generate_sample_data.py` | Synthetic data via Geometric Brownian Motion (with deliberate dirty rows) |
| `main.py` | `argparse` CLI orchestrating the pipeline |
| `dashboard.py` | Streamlit + Plotly UI |

---

## 8. Virtual Simulation – How the "Financial Analysis System" Works

Think of the project as a mini version of what an analyst desk does every morning:

1. **Data is fetched or loaded** – `yfinance` calls Yahoo Finance's public endpoint, just as a Bloomberg terminal pulls a price feed. If it fails, the system "fails over" to cached data, like a production system using a backup feed.
2. **Price movement is analysed** – daily return `r_t = P_t / P_(t-1) − 1` converts prices into comparable % moves. A ₹100 stock moving ₹5 and a ₹1000 stock moving ₹5 are very different – returns fix that.
3. **Moving averages show trend** – a 20-day SMA smooths out daily noise. Price above SMA20 above SMA50 = strong uptrend. When SMA20 crosses above SMA50 → *golden cross* (bullish); below → *death cross* (bearish).
4. **Volatility shows risk** – standard deviation of daily returns × √252 gives annual volatility. ~20% = moderate for a large-cap stock; 50%+ is very risky. Drawdown shows the worst "pain" an investor would have felt.
5. **Daily returns show performance** – the distribution chart shows how often big up/down days occur; the 5th percentile is the 95% VaR ("on 1 day in 20 you lose at least this much").
6. **Insights are generated** – `generate_insights()` applies rules (e.g. Sharpe ≥ 1 → "good risk-adjusted return") to produce sentences, like an analyst writing a note.

**Try these simulations:**
```bash
python main.py --ticker AAPL                       # steady large-cap
python main.py --ticker TSLA                       # high volatility – compare risk level
python main.py --ticker RELIANCE.NS --start 2020-01-01 --end 2024-12-31   # includes COVID crash → big drawdown
python main.py --offline                           # simulate network outage → fallback
```
Compare the reports: TSLA will show much higher volatility and drawdown than AAPL – that's risk analysis in action.

**Save for GitHub:** all PNGs in `images/`, `reports/<T>_report.md`, `reports/<T>_summary.csv`, a terminal screenshot, and a dashboard screenshot.

---

## 9. How to Run

```bash
python main.py                    # default: AAPL 2023-01-01 → 2024-12-31
python main.py --help             # all options
streamlit run dashboard.py        # dashboard at http://localhost:8501
jupyter notebook notebooks/stock_analysis_eda.ipynb
```

**Expected terminal output (abridged):**
```
=== Stock Market Data Analyzer ===

[INFO] Downloading AAPL from Yahoo Finance (2023-01-01 -> 2024-12-31) ...
[INFO] Raw data saved to data/AAPL_raw.csv
[INFO] Source: Yahoo Finance (yfinance) | 501 rows loaded
[INFO] Data cleaning summary:
       Rows before cleaning : 501
       Duplicates removed   : 0
       ...
[CHART] Saved images/AAPL_closing_price.png
... (7 charts)
[REPORT] Saved reports/AAPL_report.md
[REPORT] Saved reports/AAPL_summary.csv

  STOCK ANALYSIS SUMMARY: AAPL
  Total return        : 101.65%
  CAGR                : 42.30%
  Annual volatility   : 21.37% (Moderate risk)
  Sharpe ratio        : 1.57
  Max drawdown        : -16.71%
  Trend               : Strong Uptrend
```

**Generated files**
| Location | Files |
|---|---|
| `images/` | `closing_price`, `moving_averages`, `daily_returns`, `return_distribution`, `volatility_drawdown`, `cumulative_return`, `monthly_heatmap` (PNG) |
| `outputs/` | `<T>_processed.csv` (all columns), `<T>_monthly_returns.csv` |
| `reports/` | `<T>_report.md`, `<T>_summary.csv` |

**Sample interpretation (AAPL 2023–24):** the stock roughly doubled (+101.6%) with moderate volatility (21%), its worst peak-to-trough fall was ~17%, and a Sharpe of 1.57 means returns comfortably compensated for risk *in that period*. (Past performance ≠ future results.)

---

## 10. GitHub Upload Steps

**Repo name:** `Stock-Market-Data-Analyzer`
**Description:** *Python tool that analyses stock price trends, returns and risk (moving averages, volatility, Sharpe, drawdown, VaR) using yfinance, pandas and Matplotlib, with auto-generated reports and a Streamlit dashboard.*
**Topics/tags:** `python` `pandas` `numpy` `matplotlib` `seaborn` `yfinance` `stock-market` `financial-analysis` `data-analysis` `data-visualization` `streamlit` `fintech` `time-series` `student-project`

1. On GitHub → **New repository** → name it, keep it **Public**, do **not** add a README (you have one).
2. In the project folder:
```bash
git init
git add .
git commit -m "Initial commit: project structure and stock analyzer pipeline"
git branch -M main
git remote add origin https://github.com/<your-username>/Stock-Market-Data-Analyzer.git
git push -u origin main
```
3. Later changes:
```bash
git add <files>
git commit -m "Add moving average crossover signals"
git push
```
4. **Screenshots:** put them in `images/` (e.g. `images/screenshots/terminal_output.png`), commit, and reference them in README with `![Terminal](images/screenshots/terminal_output.png)`.
5. Add the description and topics via the ⚙️ next to **About** on the repo page. Pin the repo on your profile.

**Good commit message style:** imperative, specific – `Add CSV fallback when yfinance fails`, not `update` or `final final`.

---

## 11. Proof-Building Strategy (6 Days)

| Day | Work | Files to commit | Commit messages | Screenshots |
|---|---|---|---|---|
| 1 – Setup | venv, folders, requirements, .gitignore, README skeleton | structure, `requirements.txt`, `.gitignore`, `src/config.py` | `Initial project structure and configuration` | Folder structure in VS Code |
| 2 – Data fetching | `data_loader.py`, sample data generator | `src/data_loader.py`, `src/generate_sample_data.py`, `data/sample_stock_data.csv` | `Add yfinance data fetching with CSV fallback` · `Add synthetic sample dataset for offline use` | Dataset preview (`df.head()`) |
| 3 – Cleaning & EDA | `data_cleaning.py`, notebook | `src/data_cleaning.py`, `notebooks/*.ipynb` | `Add data cleaning and validation` · `Add EDA notebook` | Cleaning log, `describe()` output |
| 4 – MAs & returns | `analysis.py` | `src/analysis.py` | `Add returns and moving average calculations` · `Add volatility, drawdown, Sharpe and VaR metrics` | Processed CSV in Excel |
| 5 – Visualization | `visualization.py`, dashboard | `src/visualization.py`, `dashboard.py`, `images/*.png` | `Add 7 analysis charts` · `Add Streamlit dashboard` | All charts, dashboard |
| 6 – Report & docs | `report.py`, `main.py`, README, docs | `src/report.py`, `main.py`, `reports/*`, `README.md`, `docs/*` | `Add automated report generation` · `Add README with screenshots and documentation` | Terminal output, report, GitHub repo page |

Post a short LinkedIn update with 2–3 charts and the repo link on Day 6.

---

## 12. Screenshots / Outputs Checklist
Save in `images/screenshots/`:

- [ ] `01_folder_structure.png` – VS Code Explorer showing the tree
- [ ] `02_dataset_preview.png` – `data/AAPL_raw.csv` or notebook `df.head()`
- [ ] `03_terminal_output.png` – full `python main.py` run
- [ ] `04_closing_price.png` – `images/AAPL_closing_price.png`
- [ ] `05_moving_averages.png` – `images/AAPL_moving_averages.png`
- [ ] `06_daily_returns.png` – daily returns + distribution charts
- [ ] `07_volatility_summary.png` – volatility/drawdown chart + Risk Summary table
- [ ] `08_final_report.png` – `reports/AAPL_report.md` rendered on GitHub
- [ ] `09_dashboard.png` – Streamlit dashboard
- [ ] `10_github_repo.png` – your repo homepage with README

> ⚠️ Educational project – not financial advice.
