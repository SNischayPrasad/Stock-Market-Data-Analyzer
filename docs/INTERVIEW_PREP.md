# Interview Preparation – Stock Market Data Analyzer

## HR Explanation (non-technical, ~45 seconds)
"I built a Python tool that analyses a company's stock price history. You type in a stock like Apple or TCS, and it automatically downloads the data, cleans it, and tells you how much the stock grew, which direction it's trending, and how risky it was – with charts and a written report. I built it because I wanted to understand how analysts make data-driven decisions, and it taught me to take messy real-world data and turn it into clear insights that a non-technical person can act on."

## Technical Explanation (~90 seconds)
"It's a modular pandas pipeline. `data_loader` pulls daily OHLCV data via yfinance, with a fallback chain – cached CSV, then a bundled synthetic dataset – so it never fails on network issues. `data_cleaning` parses dates, sorts, removes duplicates, coerces types, forward-fills missing prices and drops invalid rows, logging each fix. `analysis` adds features: daily, cumulative and log returns via `pct_change`; 20/50/200-day SMAs and a 20-day EMA with `rolling` and `ewm`; golden/death-cross signals; rolling annualised volatility (std × √252) and drawdown via `cummax`. It then computes CAGR, Sharpe ratio, max drawdown and 95% historical VaR. `visualization` saves seven Matplotlib/Seaborn charts, and `report` generates rule-based insights into Markdown and CSV. `main.py` is an argparse CLI, and a Streamlit dashboard reuses the same modules, so there's a single source of truth for calculations."

---

## 10 Interview Questions with Strong Answers

### 1. Explain your project.
"Stock Market Data Analyzer is a Python project that automates basic equity analysis. Given a ticker and a date range, it **collects** data from Yahoo Finance (with CSV fallback), **cleans** it, calculates **returns, moving averages, volatility, drawdown, Sharpe ratio and Value-at-Risk**, generates **seven charts**, and writes a **report with plain-English insights**. For example, for Apple from 2023 to 2024 it found a 101% total return, 21% annualised volatility – moderate risk – a maximum drawdown of about 17% and a Sharpe of 1.57. I structured it as separate modules for each pipeline stage, added a CLI and an optional Streamlit dashboard. It's educational – not financial advice – but it uses the same metrics analysts and FinTech apps use."

### 2. Why did you use daily returns instead of raw prices?
"Prices aren't comparable – a ₹10 move means different things for a ₹100 and a ₹3000 stock. Returns normalise movement into percentages, so you can compare stocks and time periods. They're also closer to stationary, which is what statistical measures like standard deviation assume."

### 3. What is a moving average and how did you use it?
"A Simple Moving Average is the mean of the last N closing prices; it smooths daily noise to reveal the trend. I calculated 20, 50 and 200-day SMAs using `df['Close'].rolling(N).mean()`. If price > SMA20 > SMA50, I label it a strong uptrend. When SMA20 crosses above SMA50 that's a golden cross (bullish signal), below is a death cross. I also added an EMA, which weights recent prices more and reacts faster. Moving averages lag, though – they confirm trends, they don't predict them."

### 4. How did you measure risk?
"Four ways. **Volatility** – standard deviation of daily returns, annualised by multiplying by √252 because variance scales with time. **Maximum drawdown** – the largest fall from a running peak, `Close / Close.cummax() − 1`, which shows the worst pain an investor felt. **Sharpe ratio** – excess return over a 4% risk-free rate divided by volatility, i.e. return per unit of risk. **95% VaR** – the 5th percentile of daily returns: on 1 day in 20, the loss is at least that much."

### 5. Why multiply by √252?
"There are about 252 trading days a year. If daily returns are independent, variance adds up over time, so annual variance = 252 × daily variance, and volatility (the square root) = daily volatility × √252. Annual returns, on the other hand, scale linearly, so the mean is multiplied by 252."

### 6. How did you clean the data and why does it matter?
"I selected required columns, converted the index to datetime and sorted it, removed duplicate dates, coerced every column to numeric so stray text became NaN, forward-filled missing prices – the standard finance convention, since the last traded price is the best estimate – and removed impossible rows like zero or negative prices. I tested this with a sample file where I deliberately injected missing values and a duplicate. A single bad row can create a fake 100% return and distort volatility, so cleaning comes first."

### 7. What happens if Yahoo Finance is down or the ticker is wrong?
"The loader returns an empty DataFrame instead of crashing, and `get_stock_data` falls back to a cached CSV from a previous run, then to a bundled sample dataset. Every downloaded file is cached automatically. The user can also pass `--csv` or `--offline`. This makes the tool reproducible and resilient – the same idea as a backup data feed in production."

### 8. What's the difference between simple and log returns? Which did you use?
"Simple return is `P_t / P_(t−1) − 1`; log return is `ln(P_t / P_(t−1))`. Simple returns aggregate across assets in a portfolio; log returns add up across time, which makes multi-period maths easier and is common in quant models. I used simple returns for reporting because they're intuitive, and stored log returns as a column for further analysis."

### 9. How is your code structured, and why?
"Each pipeline stage is its own module in `src/` – loader, cleaning, analysis, visualization, report – with settings centralised in `config.py`. `main.py` only orchestrates. This separation of concerns means I could build the Streamlit dashboard by reusing the same functions without duplicating logic, each piece can be tested independently, and changing, say, the moving-average window is a one-line change in config."

### 10. What are the limitations, and how would you improve it?
"It's descriptive, not predictive – historical volatility and moving averages don't forecast the future, and crossover signals generate false alarms in sideways markets. VaR assumes the past distribution repeats and understates tail risk. Improvements I'd make: benchmark against an index like NIFTY 50 to compute beta and alpha, add RSI/MACD/Bollinger Bands, backtest the crossover strategy including transaction costs, compare multiple stocks with a correlation matrix, add pytest unit tests with GitHub Actions, and deploy the dashboard on Streamlit Cloud."

---

## Bonus Quick-Fire Questions
| Question | Short answer |
|---|---|
| What is CAGR? | Constant annual growth rate that turns the start value into the end value: `(End/Start)^(1/years) − 1` |
| What does `pct_change()` do? | `(current − previous) / previous` for each row |
| Why are the first 49 rows of SMA_50 NaN? | Not enough history yet for a 50-day window – expected behaviour |
| `ffill` vs `dropna`? | ffill keeps the row using last known value; dropna removes it (loses data, breaks continuity) |
| What is OHLCV? | Open, High, Low, Close, Volume – one row per trading day |
| Adjusted close? | Close adjusted for splits and dividends – better for long-term return comparisons |
| Is a Sharpe of 1.57 good? | Above 1 is generally considered good, but it's backward-looking and period-dependent |

## Tips
- Have the GitHub repo and one chart open on your phone/laptop.
- Lead with the **problem → what you built → result → what you learned**.
- Always say *"it's an educational tool, not investment advice"* – it shows maturity.
- Be ready to open `analysis.py` and explain any line.
