import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

st.title("📈 Stock Dashboard")
st.write("Live stock data powered by Yahoo Finance")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
period = st.sidebar.selectbox("Time Period", ["1d", "5d", "1mo", "3mo", "6mo", "1y"])

data = yf.Ticker(ticker).history(period=period)
st.subheader(f"{ticker} Closing Price")
st.line_chart(data['Close'])

col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${data['Close'][-1]:.2f}")
col2.metric("Highest", f"${data['Close'].max():.2f}")
col3.metric("Lowest", f"${data['Close'].min():.2f}")

# Raw data
if st.checkbox("Show raw data"):
    st.dataframe(data)

    # Daily returns chart
st.subheader("Daily Returns (%)")
returns = data['Close'].pct_change() * 100
st.line_chart(returns)

# Summary stats
st.subheader("Summary Statistics")
st.dataframe(data['Close'].describe().round(2))

