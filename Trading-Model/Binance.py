import requests 
import json
import decimal
import hmac
import time
import pandas as pd

binance_keys = {
	'api_key': "PASTE API KEY HERE",
	'secret_key': "PASTE SECRET KEY HERE"
}

class Binance:
	def __init__(self):

		self.base = 'https://api.binance.com'

		self.endpoints = {
			"order": '/api/v3/order',
			"testOrder": '/api/v3/order/test',
			"allOrders": '/api/v3/allOrders',
			"klines": '/api/v3/klines',
			"exchangeInfo": '/api/v3/exchangeInfo'
		}

    self.headers = {"X-MBX-APIKEY": binance_keys['api_key']}

	def GetTradingSymbols(self, quoteAssets=None):
		''' Gets All symbols which are tradable (currently) '''
		url = self.base + self.endpoints["exchangeInfo"]

		try: 
			response = requests.get(url)
			data = json.loads(response.text)
		except Exception as e:
			print(" Exception occured when trying to access "+url)
			print(e)
			return []

		symbols_list = []

		for pair in data['symbols']:
			if pair['status'] == 'TRADING':
        if quoteAssets != None and pair['quoteAsset'] in quoteAssets:
				symbols_list.append(pair['symbol'])

		return symbols_list

	def GetSymbolData(self, symbol, interval):
		''' Gets trading data for one symbol '''

		params = '?&symbol='+symbol+'&interval='+interval

		url = self.base + self.endpoints['klines'] + params

		# download data
		data = requests.get(url)
		dictionary = json.loads(data.text)

		# put in dataframe and clean-up
		df = pd.DataFrame.from_dict(dictionary)
		df = df.drop(range(6, 12), axis=1)

		# rename columns
		col_names = ['time', 'open', 'high', 'low', 'close', 'volume']
		df.columns = col_names

		# transform values from strings to floats
		for col in col_names:
			df[col] = df[col].astype(float)

    # create a date column
    df['date'] = pd.to_datetime(df['time'] * 1000000, infer_datetime_format=True)

		return df


	def PlaceOrder(self, symbol, side, type, quantity=0, price=0, test):

		'''
		Symbol: The symbol for which to get the trading pair eg. ETHBTC	
      ETH - base Asset (Buying)
      BTC - quote Asset (Selling)

    side: 'Buy or Sell'

    type: order type, MARKET, LIMIT, STOP LOSS 

		quantity: ...
		'''

		params = {
			'symbol': symbol,
			'side': side,
			'type': type,
			'timeInForce': 'GTC',
			'quantity': quantity,
			'price' : self.floatToString(price),
			'recvWindow': 5000,
			'timestamp': int(round(time.time()*1000))
		}

    if type != 'MARKET':
      params['timeInForce'] = 'GTC'
      params['price'] = self.floatToString(price)

		self.signRequest(params)

		url = ''
		if test: 
			url = self.base + self.endpoints['testOrder']
		else:
			url = self.base + self.endpoints['order']


		try: 
			response = requests.post(url, params=params, headers=self.headers)
      data = response.text
		except Exception as e:
			print(" Exception occured when trying to place order on "+url)
			print(e)
			data = {'code': '-1', 'msg':e}
			return None

		return json.loads(data)

	def CancelOrder(self, symbol, orderId):
		'''
			Cancels the order on a symbol based on orderId
		'''

		params = {
			'symbol': symbol,
			'orderId' : orderId,
			'recvWindow': 5000,
			'timestamp': int(round(time.time()*1000))
		}

		self.signRequest(params)

		url = self.base + self.endpoints['order']

		try: 
			response = requests.delete(url, params=params, headers=self.headers)
      data = response.text
		except Exception as e:
			print(" Exception occured when trying to cancel order on "+url)
			print(e)
			date = {'code': '-1', 'msg':e}
		
    return json.loads(data)

	def GetOrderInfo(self, symbol, orderId):
		'''
			Gets info about an order on a symbol based on orderId
		'''

		params = {
			'symbol': symbol,
			'orderId' : orderId,
			'recvWindow': 5000,
			'timestamp': int(round(time.time()*1000))
		}

		self.signRequest(params)

		url = self.base + self.endpoints['order']

		try: 
			response = requests.get(url, params=params, headers=self.headers)
      data = response.text
		except Exception as e:
			print(" Exception occured when trying to get order info on "+url)
			print(e)
			data = {'code': '-1', 'msg':e}

		return json.loads(data)


	def GetAllOrderInfo(self, symbol):
		'''
			Gets info about all order on a symbol
		'''

		params = {
			'symbol': symbol,
			'timestamp': int(round(time.time()*1000))
		}

		self.signRequest(params)

		url = self.base + self.endpoints['allOrders']

		try: 
			response = requests.get(url, params=params, headers=self.headers)
      data = response.text
		except Exception as e:
			print(" Exception occured when trying to get info on all orders on "+url)
			print(e)
			data = {'code': '-1', 'msg':e}

		return json.loads(data)

	def floatToString(self, f):
		''' Converts the given float to a string,
		without resorting to the scientific notation '''

		ctx = decimal.Context()
		ctx.prec = 12
		d1 = ctx.create_decimal(repr(f))
		return format(d1, 'f')

	def signRequest(self, params):
		''' Signs the request to the Binance API '''

		query_string = '&'.join(["{}={}".format(d, params[d]) for d in params])
		signature = hmac.new(binance_keys['secret_key'].encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
		params['signature'] = signature.hexdigest()







