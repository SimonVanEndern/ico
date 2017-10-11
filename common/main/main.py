from common.coinmarketCapApi import CoinmarketCapApi
from finance.analysis.coinmarket_start_time import AggregateCoinmarketStartTime


class Main:
    print("Aggregation started")

    coinmarketcap = CoinmarketCapApi()

    AggregateCoinmarketStartTime(coinmarketcap)

    # AggregateAverageMarketCapitalization(coinmarketcap)


Main()
