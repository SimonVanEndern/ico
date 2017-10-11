from common.coinmarketCapApi import CoinmarketCapApi
from common.currency_handler import CurrencyHandler
from finance.analysis.coinmarket_start_time import AggregateCoinmarketStartTimeAndAverageVolume


class Main:
    print("Aggregation started")

    coinmarketcap = CoinmarketCapApi()
    currency_handler = CurrencyHandler()

    AggregateCoinmarketStartTimeAndAverageVolume(coinmarketcap, currency_handler)


Main()
