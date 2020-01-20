class Strategies:

	@staticmethod
	def maStrategy(df, i):
		''' If price is 10% below the Slow MA, return True'''

		buy_price = 0.98 * df['slow_sma'][i]
		if buy_price >= df['close'][i]:
			return min(buy_price, df['high'][i])

		return False

	@staticmethod
	def bollStrategy(df, i):
		''' If price is 2.5% below the Lower Bollinger Band, return True'''

		buy_price = 0.995 * df['low_boll'][i]
		if buy_price >= df['close'][i]:
			return min(buy_price, df['high'][i])

		return False
