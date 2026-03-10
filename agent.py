import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.express as px

# Set page configuration
st.set_page_config(page_title="Nasdaq Agent Dashboard", layout="wide")

# Title
st.title("Nasdaq Agent Base Dashboard")

# Sidebar for user inputs
st.sidebar.header("Nasdaq Data Explorer")
nasdaq_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'TSLA', 'NVDA', 'AMD', 'INTC', 'NFLX']
selected_ticker = st.sidebar.selectbox("Select Nasdaq Ticker", nasdaq_tickers)
period_options = ['1mo', '3mo', '6mo', '1y', '2y', '5y']
selected_period = st.sidebar.selectbox("Select Period", period_options)
interval_options = ['1d', '1wk', '1mo']
selected_interval = st.sidebar.selectbox("Select Interval", interval_options)

# Fetch data from Yahoo Finance (Nasdaq)
@st.cache_data
def fetch_nasdaq_data(ticker, period, interval):
    data = yf.download(ticker, period=period, interval=interval)
    if data is not None and not data.empty:
        data.reset_index(inplace=True)
    return data

df = fetch_nasdaq_data(selected_ticker, selected_period, selected_interval)

if df is not None and not df.empty:
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    latest_close = df['Close'].iloc[-1]
    min_close = df['Close'].min()
    max_close = df['Close'].max()
    vol_sum = df['Volume'].sum()
    with col1:
        st.metric("Latest Close", f"${latest_close:,.2f}")
    with col2:
        st.metric("52W Low (Period Min)", f"${min_close:,.2f}")
    with col3:
        st.metric("52W High (Period Max)", f"${max_close:,.2f}")
    with col4:
        st.metric("Total Volume", f"{vol_sum:,}")

    # Time Series Line Chart
    st.subheader(f"{selected_ticker} Price Over Time")
    fig = px.line(df, x='Date', y='Close', title=f"{selected_ticker} Closing Price", markers=True)
    st.plotly_chart(fig, use_container_width=True)

    # Candlestick Chart
    st.subheader(f"{selected_ticker} OHLC Candlestick")
    fig_candle = px.line(df, x='Date', y=['Open', 'High', 'Low', 'Close'], title="OHLC Data")
    st.plotly_chart(fig_candle, use_container_width=True)

    # Volume bar chart
    st.subheader(f"{selected_ticker} Volume Over Time")
    fig_vol = px.bar(df, x='Date', y='Volume', title="Volume Traded")
    st.plotly_chart(fig_vol, use_container_width=True)

    # Data table
    st.subheader(f"{selected_ticker} Data Table")
    st.dataframe(df, use_container_width=True)
else:
    st.warning("No data fetched for the selected NASDAQ ticker and period.")
