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
