import pandas as pd
import requests
import json


class TradingModel:

  def __init__(self, symbol):
    self.symbol = symbol
    self.df = self.getData()

  def getData(self):
    base = 'https://api.binance.com'
    endpoint = '/api/v3/klines'
    params = '?&symbol='+self.symbol+'&interval=1h'

    url = base + endpoint+ params

    data = requests.get(url)
    dictionary = json.loads(data.text)

    df = pd.DataFrame.from_dict(dictionary)
    df = df.drop(range(6, 12), axis=1)

    col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
    df.columns = col_names

    print(df)

    return df


def Main():
    symbol = "BTCUSDT"
    model = TradingModel(symbol)
    model.getData()

if __name__== '__main__':
    Main()
