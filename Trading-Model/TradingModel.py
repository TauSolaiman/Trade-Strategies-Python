import pandas as pd
import requests
import json

import plotly.graph_objs as go
from plotly.offline import plot

#Using Binance class to grab symbol data
from Binance import Binance

class TradingModel:
	
	def __init__(self, symbol, timeframe='4h'):
		self.symbol = symbol
		self.timeframe = timeframe
		self.exchange = Binance()
		self.df = self.exchange.GetSymbolData(symbol, timeframe)
		self.last_price = self.df['close'][len(self.df['close'])-1]

	#Looking directly into the dataframe to see what indicators to plot 

	def plotData(self, buy_signals = False, sell_signals = False, plot_title=""):
		df = self.df

		# plot candlestick chart
		candle = go.Candlestick(
			x = df['time'],
			open = df['open'],
			close = df['close'],
			high = df['high'],
			low = df['low'],
			name = "Candlesticks")

		data = [candle]

		# plot MAs
		if df.__contains__('fast_sma'):
			fsma = go.Scatter(
				x = df['time'],
				y = df['fast_sma'],
				name = "Fast SMA",
				line = dict(color = ('rgba(102, 207, 255, 50)')))
			data.append(fsma)

		if df.__contains__('slow_sma'):
			ssma = go.Scatter(
				x = df['time'],
				y = df['slow_sma'],
				name = "Slow SMA",
				line = dict(color = ('rgba(255, 207, 102, 50)')))
			data.append(ssma)

		if df.__contains__('low_boll'):
			lowbb = go.Scatter(
				x = df['time'],
				y = df['low_boll'],
				name = "Lower Bollinger Band",
				line = dict(color = ('rgba(255, 102, 207, 50)')))
			data.append(lowbb)

		if buy_signals:
			buys = go.Scatter(
					x = [item[0] for item in buy_signals],
					y = [item[1] for item in buy_signals],
					name = "Buy Signals",
					mode = "markers",
          marker_size = 10
				)
			data.append(buys)

		if sell_signals:
			sells = go.Scatter(
					x = [item[0] for item in buy_signals],
					y = [item[1] for item in buy_signals],
					name = "Sell Signals",
					mode = "markers",
          marker_size = 10
				)
			data.append(sells)


		# style and display
		layout = go.Layout(title = plot_title)
		fig = go.Figure(data = data, layout = layout)

		plot(fig, filename='graphs/'+plot_title+'.html')


