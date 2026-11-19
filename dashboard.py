"""
dashboard.py - optional interactive Streamlit dashboard
=======================================================
Run with:
    streamlit run dashboard.py

Reuses the SAME modules as main.py (load -> clean -> analyse), so the
numbers in the dashboard always match the CLI report.

DISCLAIMER: Educational project. Not financial advice.
"""

from datetime import date

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from src import config
from src.analysis import compute_summary, run_full_analysis
from src.data_cleaning import clean_stock_data
from src.data_loader import get_stock_data

st.set_page_config(page_title="Stock Market Data Analyzer", layout="wide")
st.title("Stock Market Data Analyzer")
st.caption("Educational project - not financial advice.")

# ---------------- Sidebar inputs ----------------
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Ticker symbol", config.DEFAULT_TICKER).upper().strip()
    start = st.date_input("Start date", date.fromisoformat(config.DEFAULT_START))
    end = st.date_input("End date", date.fromisoformat(config.DEFAULT_END))
    offline = st.checkbox("Offline mode (use sample/cached CSV)", value=False)
    uploaded = st.file_uploader("...or upload your own CSV", type="csv")


@st.cache_data(show_spinner="Fetching data...")
def load(ticker, start, end, offline):
    raw, source = get_stock_data(ticker, str(start), str(end), offline=offline)
    return raw, source


if uploaded is not None:
    raw = pd.read_csv(uploaded, parse_dates=["Date"], index_col="Date")
    source = f"Uploaded CSV ({uploaded.name})"
else:
    raw, source = load(ticker, start, end, offline)

if raw.empty:
    st.error("No data found. Check the ticker symbol or upload a CSV.")
    st.stop()

df, log = clean_stock_data(raw)
df = run_full_analysis(df)
s = compute_summary(df, ticker)
st.info(f"Data source: {source} - {s['trading_days']} trading days")

# ---------------- KPI cards ----------------
c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Last close", f"{s['last_close']:.2f}", f"{s['total_return']*100:.1f}% total")
c2.metric("CAGR", f"{s['cagr']*100:.2f}%")
c3.metric("Annual volatility", f"{s['annual_volatility']*100:.1f}%", s["risk_level"],
          delta_color="off")
c4.metric("Max drawdown", f"{s['max_drawdown']*100:.1f}%")
c5.metric("Sharpe ratio", f"{s['sharpe_ratio']:.2f}")
st.write(f"**Trend:** {s['trend']}  |  **Last signal:** {s['last_signal']}")

# ---------------- Charts ----------------
tab1, tab2, tab3, tab4 = st.tabs(["Price & MAs", "Candlestick", "Returns", "Risk"])

with tab1:
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Close"))
    for col in [f"SMA_{config.SHORT_WINDOW}", f"SMA_{config.LONG_WINDOW}",
                f"SMA_{config.TREND_WINDOW}"]:
        fig.add_trace(go.Scatter(x=df.index, y=df[col], name=col.replace("_", " ")))
    st.plotly_chart(fig, width="stretch")

with tab2:
    fig = go.Figure(go.Candlestick(x=df.index, open=df["Open"], high=df["High"],
                                   low=df["Low"], close=df["Close"]))
    fig.update_layout(xaxis_rangeslider_visible=False)
    st.plotly_chart(fig, width="stretch")

with tab3:
    st.plotly_chart(go.Figure(go.Histogram(x=df["Daily_Return"] * 100, nbinsx=60))
                    .update_layout(xaxis_title="Daily return (%)"), width="stretch")
    st.line_chart(df["Cumulative_Return"] * 100)

with tab4:
    st.line_chart(df["Rolling_Volatility"] * 100)
    st.area_chart(df["Drawdown"] * 100)

with st.expander("Show processed data"):
    st.dataframe(df.tail(100))
    st.download_button("Download processed CSV", df.to_csv().encode(), f"{ticker}_processed.csv")
