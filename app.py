import streamlit as st
import requests
import pandas as pd

st.title("📈 Stock Dashboard")
st.write("Live stock data powered by Alpha Vantage")

API_KEY = "5USJ3QIQ664Z3LMS"

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL")
period = st.sidebar.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y"])

period_map = {"1mo": "30", "3mo": "90", "6mo": "180", "1y": "365"}
days = int(period_map[period])

url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={ticker}&apikey={API_KEY}"
response = requests.get(url)
json_data = response.json()

if "Time Series (Daily)" in json_data:
    df = pd.DataFrame(json_data["Time Series (Daily)"]).T
    df.index = pd.to_datetime(df.index)
    df = df.sort_index()
    df["close"] = df["4. close"].astype(float)
    df = df.tail(days)

    st.subheader(f"{ticker} Closing Price")
    st.line_chart(df["close"])

    col1, col2, col3 = st.columns(3)
col1.metric("Current Price", f"${df['close'].iloc[-1]:.2f}")
col2.metric("Highest", f"${df['close'].max():.2f}")
col3.metric("Lowest", f"${df['close'].min():.2f}")

    st.subheader("Daily Returns (%)")
    returns = df["close"].pct_change() * 100
    st.line_chart(returns)

    if st.checkbox("Show raw data"):
        st.dataframe(df[["close"]])
else:
    st.error("Could not fetch data. Check ticker symbol.")
