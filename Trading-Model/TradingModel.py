import pandas as pd
import requests
import json

from plotly.offline import plot
import plotly.graph_objs as go

from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.bollinger_bands import lower_bollinger_band as lbb

#Using Binance Class to download data for a symbol
from Binance import Binance 

class TradingModel:

  def __init__(self, symbol):
    self.symbol = symbol
    self.exchange = Binance()
    self.df = self.exchange.GetSymbolData(symbol, '1h')
    self.last_price = self.df['close'][len(self.df['close'])-1]
    self.buy_signals = []

    try:
      # add moving averages and lower bollinger band
      self.df['fast_sma'] = sma(self.df['close'].tolist(), 10)
      self.df['slow_sma'] = sma(self.df['close'].tolist(), 30)
      self.df['low_boll'] = lbb(self.df['close'].tolist(), 14)
    except Exception as e:
      print('Exception raised when trying to computer indicators on'+ self.symbol)
      print(e)
      return None



  # define URL
  def getData(self):
    base = 'https://api.binance.com'
    endpoint = '/api/v3/klines'
    params = '?&symbol='+self.symbol+'&interval=1h'

    url = base + endpoint+ params

  #download data
    data = requests.get(url)
    dictionary = json.loads(data.text)

  # put in dataframe
    df = pd.DataFrame.from_dict(dictionary)
    df = df.drop(range(6, 12), axis=1)

  #rename columns
    col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = col_names

  #converting strings to float
    for col in col_names:
      df[col] = df[col].astype(float)

    print(df)
    
    return df

  def strategy(self):
    df = self.df

    buy_signals = []

    for i in range (1, len(df['close'])):
      if df['slow_sma'][i] > df['close'][i] and (df['slow_sma'][i] - df['close'][i]) > 0.03 * df['close'][i]:
        buy_signals.append([df['time'][i], df['low'][i]])

    self.plotData(buy_signals = buy_signals)
    


  def plotData(self, buy_signals = False):
      df = self.df

      # plot candlestick chart
      candle = go.Candlestick(
        x = df['time'],
        open = df['open'],
        close = df['close'],
        high = df['high'],
        low = df['low'],
        name = "Candlesticks")

      # plot MAs
      fsma = go.Scatter(
        x = df['time'],
        y = df['fast_sma'],
        name = 'Fast SMA',
        line = dict(color = ('rgba(102, 207, 255, 50)')))

      ssma = go.Scatter(
        x = df['time'],
        y = df['slow_sma'],
        name = 'Slow SMA',
        line = dict(color = ('rgba(255, 207, 102, 50)')))

      data = [candle, ssma, fsma]

      if buy_signals:
        buys = go.Scatter(
          x = [item[0] for item in buy_signals],
          y = [item[1] for item in buy_signals],
          name = 'Buy Signals',
          mode = "markers",
        )
        sells = go.Scatter(
          x = [item[0] for item in buy_signals],
          y = [item[1]*1.02 for item in buy_signals],
          name = 'Sell Signals',
          mode = "markers",
        )
      data = [candle, ssma, fsma, buys, sells]

      #style & display
      layout = go.Layout(title = self.symbol)
      fig = go.Figure(data = data, layout = layout)

      plot(fig, filename = self.symbol)

# Moving average and Bollinger Band Strategy
  def maStrategy(self, i:int):
    ''' If price is 10% below slow moving average, put a buy signal'''
    df = self.df
    buy_price = 0.9 * df['slow_sma'][i]
    if buy_price >= df['close'][i]:
      self.buy_signals.append(df['time'], df['close'][i], df['close'][i] * 1.045)
      return True
    
    return False

  def bollStrategy(self, i:int):
    ''' if price is 5% below lower bollinger band put a buy signal'''
    df = self.df
    buy_price = 0.95 * df['low_boll'][i]
    if buy_price >= df['close'][i]:
      self.buy_signals.append(df['time'], df['close'][i], df['close'][i] * 1.045)
      return True
    
    return False    


def Main():
    symbol = "BTCUSDT"
    model = TradingModel(symbol)
    model.strategy()

if __name__== '__main__':
    Main()
