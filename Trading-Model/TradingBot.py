from StrategyEvaluator import StrategyEvaluator
from Strategies import Strategies
from Binance import Binance
from TradingModel import TradingModel

import json
from decimal import Decimal, getcontext

def BackTestStrategies(symbols=[], interval='4h', plot=False, strategy_evaluators=[],
options = dict(starting_balance=100, initial_profits=1.02, initial_stop_loss=0.9, 
incremental_profits=1.01, incremental_stop_loss=0.98)):
  coins_tested = 0

  for symbol in symbols:
    print(symbol)
    model = TradingModel(symbol=symbol, timeframe=interval)
    for evaluator in strategy_evaluators:
      resulting_balance = evaluator.backtest(
        model,
        starting_balance = options.starting_balance,
        initial_profits = options.initial_profits,
        initial_stop_loss = options.initial_stop_loss,
        incremental_profits = options.incremental_profits,
        incremental_stop_loss = options.incremental_stop_loss,
      )

      if resulting_balance != trade_value:
        print(evaluator.strategy.__name__
        + ": starting value:" + str(options.starting_balance)
        + ": resulting balance:" + str(round(resulting_balance, 2))
        )

        if plot:
          model.plotData(
            buy_signals = evaluator.results[model.symbol]['buy_times'],
            sell_signals= evaluator.results[model.symbol]['sell_times'],
            plot_title= evaluator.strategy.__name__+ "on"+model.symbol)
          
        evaluator.profits_list.append(resulting_balance - trade_value)
        evaluator.updateResult(trade_value, resulting_balance)

      coins_tested = coins_tested + 1 

  for evaluator in strategy_evaluators:
    print("")
    evaluator.printResults()

strategy_matched_symbol = "\n Strategy Matched Symbol! \
\n Type 'b' and then press ENTER to backtest the strategy on this symbol and see the plot \
\n Type 'p' and then press ENTER to place an order \
\n Typing anything else or pressing ENTER directly will skip placing an order this time.\n"

ask_place_order = "\nType 'p' and then press ENTER to place an order \
\n Typing anything else or pressing ENTER directly will skip placing an order this time.\n"

# Function that checks current market conditions and places orders if conditions are appropriate
def EvaluateStrategies(symbols=[], strategy_evaluators=[], timeframe="1h"):
  for symbol in symbols:
    print(symbol)
    model = TradingModel(symbol=symbol, timeframe=timeframe)
    for evaluator in strategy_evaluators:
      if evaluator.evaluate(model):
        print("\n" + evaluator.strategy.__name__+"matched on"+symbol)
        print(strategy_matched_symbol)
        answer = input()

      if answer == 'b':
        resulting_balance = evaluator.backtest(
        model,
          starting_balance = options.starting_balance,
          initial_profits = options.initial_profits,
          initial_stop_loss = options.initial_stop_loss,
          incremental_profits = options.incremental_profits,
          incremental_stop_loss = options.incremental_stop_loss,
        )
        model.plotData(
          buy_signals = evaluator.results[model.symbol]['buy_times'],
          sell_signals = evaluator.results[model.symbol]['sell_times'],
          plot_title = evaluator.strategy.__name__+"matched on"+symbol
        )
        print(evaluator.result[model.symbol])
        print(ask_place_order)
        answer = input()

      if answer == 'p':
        print('Placing Buy Order')
        order_result = model.exchange.PlaceOrder(model.symbol, "BUY", "MARKET", quantity=0.02, test=False)
        if "code" in order_result:
          print("\n ERROR")
          print(order_result)
        else:
          print('SUCCESS')
          print(order_result)
          
def Main():
  #get all symbols trading against BTC and USDT and use them to backtest our strategies on a 4h minute interval
  exchange = Binance()
  symbols = exchange.GetTradingSymbols(quoteAssets=["BTC", "USDT"])

  trade_value = 100

  strategy_evaluators = [
    StrategyEvaluator( strategy_function = Strategies.bollStrategy, strategy_settings={"indicators": ['low_boll']}),
    StrategyEvaluator( strategy_function = Strategies.maStrategy, strategy_settings={"indicators": ['slow_sma']})
  ]

  BackTestStrategies(symbols=symbols, interval='4h', plot=True)

if __name__ == '__main__':
  Main()
