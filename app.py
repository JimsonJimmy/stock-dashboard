import streamlit as st
import yfinance as yf
import pandas as pd
import time

st.title("📈 Stock Dashboard")
st.write("Live stock data powered by Yahoo Finance")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y"])

try:
    time.sleep(2)
    data = yf.Ticker(ticker).history(period=period)
    
    if data.empty:
        st.error("No data found. Try a different ticker.")
    else:
        st.subheader(f"{ticker} Closing Price")
        st.line_chart(data['Close'])

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${data['Close'][-1]:.2f}")
        col2.metric("Highest", f"${data['Close'].max():.2f}")
        col3.metric("Lowest", f"${data['Close'].min():.2f}")

        st.subheader("Daily Returns (%)")
        returns = data['Close'].pct_change() * 100
        st.line_chart(returns)

        if st.checkbox("Show raw data"):
            st.dataframe(data)

except Exception as e:
    st.error("Could not fetch data. Yahoo Finance may be rate limiting. Try again in a moment.")
    st.button("Retry")
