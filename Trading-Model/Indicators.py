# class used to compute indicators on dataframe
# Import indicators from pyti as well as write function for computing indicators

from pyti.smoothed_moving_average import smoothed_moving_average as sma
from pyti.exponential_moving_average import exponential_moving_average as ema
from pyti.bollinger_bands import lower_bollinger_bands as lbb
from pyti.bollinger_bands import upper_bollinger_bands as ubb


def ComputeIchimokuCloud(df):
  #Tenkan-sen (conversion line): (9 period high + 9 period low)/2
  nine_period_high = df['high'].rolling(window=9).max()
  nine_period_low = df['low'].rolling(window=9).min()
  df['tenkansen'] = (nine_period_high + nine_period_low)/2

  #Kijun-sen (base line): (26 period high + 26 period low)/2
  period26_high = df['high'].rolling(window=26).max()
  period26_low = df['low'].rolling(window=26).min()
  df['kijunsen'] = (period26_high + period26_low)/2

  #Senkou span A (Leading Span A): (Conversion Line + Base Line)/2
  df['senkou_a'] = ((df['tenkansen'] + df['kijunsen'])/2).shift(26)

  #Senkou span B 
  period52_high = df['high'].rolling(window=52).max()
  period52_low = df['low'].rolling(window=52).min()
  df['senkou_b'] = (period52_high + period52_low)/2

  #Chikou span: the most recent closing price plotted, plotted 26 periods behind
  df['chikouspan'] = df['close'].shift(-26)

  return df



#Function for computing any indicator that we want and add it the dataframe, passed to trading model to compute a strategy

class Indicators:

  INDICATORS_DICT = {
    "sma": sma,
    "ema": ema,
    "lbb": lbb,
    "ubb": ubb,
    "ichimoku": ComputeIchimokuCloud
  }

  @staticmethod
  def AddIndicator(df, indicator_name, column_name, args):
    # df is the dataframe to which we will add the indicator
    # indicator_name is the name of indicator as found in the dict above
    # col_name is thename that the indicator will appear under in the dataframe
    # args are the arguments that might be used when calling the indicator function
    try:
      if indicator_name == "ichimoku":
        df = ComputeIchimokuCloud(df)
      else:
        df[col_name] = Indicators.INDICATORS_DICT[indicator_name](df['close'].tolist(), args)
    except Exception as e:
      print("\n Exception raised when trying to compute " indicator_name)
      print(e)


