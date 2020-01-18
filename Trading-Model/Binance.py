import pandas as pd
import requests
import json
import decimal
import hmac
import time

binance_keys = {
  'api_key': "PASTE API KEY HERE",
  'secret_key': "PASTE SECRET KEY HERE"
}


class Binance:
  def __init__(self):

    self.base = 'https://api.binance.com'

    self.endpoints = {
      "order": 'api/v1/order',
      "testOrder": 'api/v1/order/test',
      "allOrders": 'api/v1/allOrders',
      "klines": 'api/v1/klines',
      "exchangeInfo": 'api/v1/exchangeInfo'
    }

  def GetTradingSymbols(self):
    # Get all symbols that are currently tradeable
    url = self.base + self.endpoints["exchangeInfo"]

    try: 
      response = requests.get(url)
      data = json.loads(response.text)
    except Exception as e:
      print('Exception ocurred while trying to access'+url)
      print(e)
      return []

    symbols_list = []

    for pair in data['symbols']:
      if pair['status'] == 'TRADING':
        symbols_list.append(pair['symbol'])

    return symbols_list

  #Get data for a single trading pair
  def GetSymbolData(self, symbol:str, interval:str):

    params = '?&symbol='+symbol+'&interval='+interval

    url = self.base + self.endpoints['klines'] + params

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

    return df

  def PlaceOrder(self, symbol:str, side:str, type:str, quantity:float, price:float, test:bool=True):
    '''
      Symbol: ETHBTC
      ETH - base asset (what we buy for)
      BTC - quote asset (what we sell for)
      quantity - how much ETH we want 
      price - how much BTC we're willing to sell it for
    '''
    params = {
      'symbol': symbol,
      'side': side,           # BUY OR SELL
      'type': type,           # MARKET, LIMIT, STOP LOSS etc. 
      'timeInForce': 'GTC',
      'quantity': quantity,
      'price': price.floatToString(price),
      'recvWindow': 5000,
      'timestamp': int(round(time.time()*1000))
    }

    self.signRequest(params)

    url = ''
    if test:
      url = self.base + self.endpoints['testOrder']
    else:
      url = self.base + self.endpoints['order']

    try:
      response = requests.post(url, params=params, headers={"X-MBX-APIKEY": binance_keys['api_key']})
    except Exception as e:
      print('Exception occured while trying to place order on'+url)
      print(e)
      response = {'code': '-1', 'msg':e}
      return None

    return json.loads(response.text)

  def CancelOrder(self, symbol:str, orderId:str):
    '''
      Cancels the order on a symbol based on orderId
    '''
    params = {
      'symbol': symbol,
      'orderId': orderId,
      'recvWindow': 5000,
      'timestamp': int(round(time.time()*1000))
    }

    self.signRequest(params)

    url = self.base + self.endpoints['order']

    try:
      response = requests.delete(url, params=params, headers={"X-MBX-APIKEY": binance_keys['api_key']})
    except Exception as e:
      print('Exception occured while trying to cancel order on'+url)
      print(e)
      response = {'code': '-1', 'msg':e}
      return None

  def GetOrderInfo(self, symbol:str, orderId:str):
    '''
      Get info about an order based on orderId
    '''
    params = {
      'symbol': symbol,
      'orderId': orderId,
      'recvWindow': 5000,
      'timestamp': int(round(time.time()*1000))
    }

    self.signRequest(params)

    url = self.base + self.endpoints['order']

    try:
      response = requests.get(url, params=params, headers={"X-MBX-APIKEY": binance_keys['api_key']})
    except Exception as e:
      print('Exception occured while trying to get order info on'+url)
      print(e)
      response = {'code': '-1', 'msg':e}
      return None

    return json.loads(response.text)

  def GetAllOrderInfo(self, symbol:str, orderId:str):
    '''
      Get info about an order based on orderId
    '''
    params = {
      'symbol': symbol,
      'timestamp': int(round(time.time()*1000))
    }

    self.signRequest(params)

    url = self.base + self.endpoints['allOrders']

    try:
      response = requests.get(url, params=params, headers={"X-MBX-APIKEY": binance_keys['api_key']})
    except Exception as e:
      print('Exception occured while trying to get info on all orders'+url)
      print(e)
      response = {'code': '-1', 'msg':e}
      return None

    return json.loads(response.text)




# Converts float to string without resorting to scientific notation
  def floatToString(self, f:float):
    ctx = decimal.Context()
    ctx.prec = 12
    d1 = ctx.create_decimal(repr(f))
    return format(d1, 'f')

# Signs request to Binance API
  def signRequest(self, params:dict):
    query_string = '&'.join(["{}={}".format(d, params[d]) for d in params])
    signature = hmac.new(binance_keys['secret_key'].encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
    params['signature'] = signature.hexdigest()









