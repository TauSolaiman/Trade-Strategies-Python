class StrategyEvaluator:
  ''' Used to evaluate the performance of strategies '''

  def __init__(self, strategy_function, strategy_settings={'indicators': ['low_ball', 'fast_sma', 'slow_sma']}):
    
    self.strategy = strategy_function
    self.settings = strategy_settings
    self.buy_times = []
    self.sell_times = []

    self.profitable_symbols = 0
    self.unprofitable_symbols = 0

    self.complete_starting_balance = 0
    self.complete_resulting_balance = 0

    self.profits_list = []
    self.results = dict()

  def backtest(self,
   model, 
   starting_balance=100,
   initial_profits = 1.045,
   initial_stop_loss = 0.85,
   incremental_profits = 1.04,
   incremental_stop_loss = 0.975):

   '''
    Funtion used to back test a strategy given a trading Model
   '''
    
