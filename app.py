import numpy as np
import pandas as pd
import plotly.graph_objects as go
import requests
import streamlit as st
from plotly.subplots import make_subplots

response = requests.get("https://stock-samples.herokuapp.com/stocks/random").json()


st.header(f"stock_name = {response['name']}")
st.header(f"symbol = {response['symbol']}")
st.header(f"start_datetime = {response['start_datetime']}")
st.header(f"end_datetime = {response['end_datetime']}")

hist = pd.DataFrame(response['stocks'])

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

close = hist['Close']
high = hist['High']
low = hist['Low']
volume = hist['Volume']

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
               y=hist.ma_5,
               line=dict(color='red', width=2),
               hoveron='points',
               name='MA_5'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=hist.ma_10,
               line=dict(color='blue', width=2),
               hoveron='points',
               name='MA_10'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=hist.ma_20,
               line=dict(color='yellow', width=2),
               hoveron='points',
               name='MA_20'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=hist.ma_60,
               line=dict(color='green', width=2),
               hoveron='points',
               name='MA_60'))
fig3.add_trace(
    go.Scatter(x=hist.index,
               y=hist.ma_120,
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
               y=np.concatenate([hist.bb_upper, hist.bb_lower[::-1]]),
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
               y=np.concatenate([hist.env_upper, hist.env_lower[::-1]]),
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

fig3.add_trace(go.Scatter(x=hist.index, y=hist.rsi, name='rsi 14'), row=2, col=1)

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

fig3.add_trace(go.Scatter(x=hist.index, y=hist.cci, name='cci 14'), row=2, col=1)

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

fig3.add_trace(go.Scatter(x=hist.index, y=hist.obv, name='obv'), row=2, col=1)

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

fig3.add_trace(go.Scatter(x=hist.index, y=hist.slowk, name='slowk'), row=2, col=1)
fig3.add_trace(go.Scatter(x=hist.index, y=hist.slowd, name='slowd'), row=2, col=1)

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

fig3.add_trace(go.Scatter(x=hist.index, y=hist.macdsignal, name='macd_signal'),
               row=2,
               col=1)
fig3.add_trace(go.Scatter(x=hist.index, y=hist.macd, name='macd'), row=2, col=1)

fig3.add_trace(go.Bar(x=hist.macdhist.index, y=hist.macdhist.values), row=2, col=1)

st.plotly_chart(fig3, use_container_width=True)
