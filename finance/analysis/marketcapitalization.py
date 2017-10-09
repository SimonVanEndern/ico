import numpy
import pandas

from common.coinmarketCapApi import CoinmarketCapApi


class MarketCapitalization:
    def __init__(self):
        self.coinmarketcap = CoinmarketCapApi()
        return

    def volume_analysis(self):
        data = self.coinmarketcap.get_market_cap()
        print(type(data[0]))
        print(data)
        df = pandas.Series(data)
        print(df.describe())
        print(pandas.Series([1, 2, 3]).astype(numpy.int64).describe())


marketcap = MarketCapitalization()
marketcap.volume_analysis()
