# Social Media Posts

Replace `<REPO_LINK>` with your GitHub repo URL before posting.

---

## LinkedIn Post

**Attach:** `images/screenshots/09_dashboard.png`, `images/AAPL_moving_averages.png`, `images/screenshots/03_terminal_output.png`. Or upload the 6 Instagram slides as a PDF carousel.

```
📈 I built a Stock Market Data Analyzer in Python, and here's what I learned about measuring risk.

Looking at a stock chart, it's easy to *feel* whether a stock is "good". Analysts don't go by feel. They measure it. So I built a tool that does exactly that.

🔧 What it does
Give it a ticker (AAPL, TCS.NS, MSFT…) and a date range, and it:
1️⃣ Pulls real price data from Yahoo Finance (with a CSV fallback so it works offline)
2️⃣ Cleans it: duplicates, missing values, invalid prices
3️⃣ Calculates daily and cumulative returns and CAGR
4️⃣ Tracks trend with 20/50/200-day moving averages and golden/death-cross signals
5️⃣ Measures risk: volatility, max drawdown, Sharpe ratio and Value-at-Risk
6️⃣ Generates 7 charts plus an automated report with plain-English insights
7️⃣ Has an interactive Streamlit dashboard

📊 Sample result: Apple (2023–2024)
• Total return: +101.6% | CAGR: 42.3%
• Annual volatility: 21.4% (moderate risk)
• Max drawdown: −16.7%
• Sharpe ratio: 1.57

💡 Key takeaways
→ Returns alone don't tell the story. Risk-adjusted return (Sharpe) and drawdown show what an investor actually had to sit through.
→ Volatility is annualised with √252 (trading days), not 365.
→ Clean data first: one bad row can fake a 100% "return".
→ Modular code paid off. The dashboard reuses the exact same analysis functions as the CLI.

🛠 Tech: Python · pandas · NumPy · Matplotlib · Seaborn · yfinance · Plotly · Streamlit

🔗 Code, docs and screenshots: <REPO_LINK>

Next up: RSI/MACD indicators, benchmarking against NIFTY 50 / S&P 500, and backtesting the crossover strategy.

I'd love feedback from anyone in finance or data analytics. What metric would you add? 👇

⚠️ Educational project only, not financial advice.

#Python #DataAnalysis #FinancialAnalysis #StockMarket #Pandas #DataVisualization #FinTech #Streamlit #DataAnalyst #StudentProject #LearningInPublic #OpenToWork
```

### Short LinkedIn version
```
Built a Stock Market Data Analyzer in Python 📈

Ticker in → returns, moving-average trends, volatility, drawdown, Sharpe ratio, VaR, 7 charts and an auto-generated report out. Plus a Streamlit dashboard.

Apple 2023–24: +101.6% return, 21.4% volatility, Sharpe 1.57.

Biggest lesson: return without risk is half the story.

Python · pandas · NumPy · Matplotlib · yfinance · Streamlit
🔗 <REPO_LINK>

Educational project, not financial advice.
#Python #DataAnalysis #FinTech #StockMarket #StudentProject
```

---

## Instagram Post

**Carousel (upload in order):** `images/social/insta_1_cover.png` → `insta_2_pipeline.png` → `insta_3_results.png` → `insta_4_moving_averages.png` → `insta_5_heatmap.png` → `insta_6_tech_cta.png` (all 1080×1080)

**Caption:**
```
I taught Python to analyse the stock market 📈🐍

Type in any stock → it pulls real data, cleans it, and tells you:
✅ how much it returned
✅ which way it's trending
✅ how risky the ride was

Tested on Apple (2023–24):
📊 +101.6% total return
📉 −16.7% worst drop from peak
⚖️ Sharpe ratio 1.57

7 charts + a full report, generated automatically in seconds.

Built with Python, pandas, Matplotlib, yfinance and Streamlit.

Full code is on GitHub. Link in bio 🔗
Save this 📌 if you're looking for your next Python project idea!

⚠️ Educational project, not financial advice.

#python #pythonprojects #coding #programming #datascience #dataanalytics #stockmarket #fintech #codinglife #studentlife #learnpython #developer #machinelearning #techstudent #100daysofcode
```

**Story idea:** Post slide 3 (results) with a poll sticker: "Would you check volatility before buying a stock? Yes / What's volatility? 😅", plus a link sticker to the repo.

**Reel idea (15–20 s):** screen-record `python main.py --ticker TSLA` running → cut to charts appearing → end on the dashboard. Text overlay: "Python analysed Tesla in 3 seconds."
