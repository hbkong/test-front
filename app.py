import numpy as np
import plotly.graph_objects as go
import streamlit as st
import talib
import yfinance as yf
from plotly.subplots import make_subplots
from talib import BBANDS, MA_Type
import requests
import json
import pandas as pd


response = requests.get("http://172.20.0.70:23052/stocks/random").text
hist = json.loads(response)
hist = pd.DataFrame(hist)


st.header("Random Candle Stick")

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

st.plotly_chart(fig3, use_container_width=True)

upper, _, lower = BBANDS(hist.Close, 20, 2, 2)

from talib import CCI, MA, MACD, OBV, RSI, SMA, STOCH

close = hist['Close']
high = hist['High']
low = hist['Low']
volume = hist['Volume']

ma_5 = MA(close, 5)
ma_10 = MA(close, 10)
ma_20 = MA(close, 20)
ma_60 = MA(close, 60)
ma_120 = MA(close, 120)

env_upper = SMA(close, 14) + SMA(close, 14) * 0.05
env_lower = SMA(close, 14) - SMA(close, 14) * 0.05

macd, macdsignal, macdhist = MACD(close,
                                  fastperiod=12,
                                  slowperiod=26,
                                  signalperiod=9)

rsi = RSI(close, 14)

cci = CCI(high, low, close, 14)

obv = OBV(close, volume)

slowk, slowd = STOCH(high,
                     low,
                     close,
                     fastk_period=5,
                     slowk_period=3,
                     slowk_matype=0,
                     slowd_period=3,
                     slowd_matype=0)

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

# Candle Stick

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

# Volume

st.header("Volume")

fig3.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume'),
               secondary_y=True)
fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

st.plotly_chart(fig3, use_container_width=True)

# Moving Average

st.header("Moving Average")

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.add_trace(
    go.Scatter(x=hist.index,
               y=ma_5,
               line=dict(color='red', width=2),
               hoveron='points',
               name='MA_5'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=ma_10,
               line=dict(color='blue', width=2),
               hoveron='points',
               name='MA_10'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=ma_20,
               line=dict(color='yellow', width=2),
               hoveron='points',
               name='MA_20'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=ma_60,
               line=dict(color='green', width=2),
               hoveron='points',
               name='MA_60'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=ma_120,
               line=dict(color='black', width=2),
               hoveron='points',
               name='MA_120'))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

st.plotly_chart(fig3, use_container_width=True)

# Bolnger Bands

st.header("Bolnger Bands")

fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.add_trace(
    go.Scatter(x=np.concatenate([hist.index, hist.index[::-1]]),
               y=np.concatenate([upper, lower[::-1]]),
               fill='toself',
               line=dict(color='yellow', width=1),
               fillcolor='rgba(255,255,0,0.2)',
               hoveron='points',
               name='BB'))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

st.plotly_chart(fig3, use_container_width=True)

# Envelope

st.header("Envelope")

fig3 = make_subplots(specs=[[{"secondary_y": True}]])
fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.add_trace(
    go.Scatter(x=np.concatenate([hist.index, hist.index[::-1]]),
               y=np.concatenate([env_upper, env_lower[::-1]]),
               fill='toself',
               line=dict(color='yellow', width=1),
               fillcolor='rgba(255,255,0,0.2)',
               hoveron='points',
               name='Envelope'))
fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

st.plotly_chart(fig3, use_container_width=True)

# RSI

st.header("RSI")

fig3 = make_subplots(rows=2,
                     cols=1,
                     specs=[[{
                         "secondary_y": True
                     }], [{
                         "secondary_y": False
                     }]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))
fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

fig3.add_trace(go.Scatter(x=hist.index, y=rsi, name='rsi 14'), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)

# CCI

st.header("CCI")

fig3 = make_subplots(rows=2,
                     cols=1,
                     specs=[[{
                         "secondary_y": True
                     }], [{
                         "secondary_y": False
                     }]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

fig3.add_trace(go.Scatter(x=hist.index, y=cci, name='cci 14'), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)

# OBV

st.header("OBV")

fig3 = make_subplots(rows=2,
                     cols=1,
                     specs=[[{
                         "secondary_y": True
                     }], [{
                         "secondary_y": False
                     }]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

fig3.add_trace(go.Scatter(x=hist.index, y=obv, name='obv'), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)

# Stochastic Slow

st.header("Stochastic Slow")

fig3 = make_subplots(rows=2,
                     cols=1,
                     specs=[[{
                         "secondary_y": True
                     }], [{
                         "secondary_y": False
                     }]])

fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

fig3.add_trace(go.Scatter(x=hist.index, y=slowk, name='slowk'), row=2, col=1)
fig3.add_trace(go.Scatter(x=hist.index, y=slowd, name='slowd'), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)

# MACD
st.header("MACD")

fig3 = make_subplots(rows=2,
                     cols=1,
                     specs=[[{
                         "secondary_y": True
                     }], [{
                         "secondary_y": False
                     }]])

# Candle Stick
fig3.add_trace(
    go.Candlestick(
        x=hist.index,
        open=hist['Open'],
        high=hist['High'],
        low=hist['Low'],
        close=hist['Close'],
    ))

fig3.update_layout(xaxis_rangeslider_visible=False)
fig3.update_yaxes(range=[0, hist.Volume.max() * 9], secondary_y=True)
fig3.update_yaxes(visible=False, secondary_y=True)
fig3.update_xaxes(rangebreaks=[
    dict(bounds=['sat', 'mon']),
])

fig3.add_trace(go.Scatter(x=hist.index, y=macdsignal, name='macd_signal'),
               row=2,
               col=1)
fig3.add_trace(go.Scatter(x=hist.index, y=macd, name='macd'), row=2, col=1)

fig3.add_trace(go.Bar(x=macdhist.index, y=macdhist.values), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)
