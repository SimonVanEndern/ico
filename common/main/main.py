import logging
import unittest

import ico.main
from common.coinmarketCapApi import CoinmarketCapApi
from common.currency_handler import CurrencyHandler
from finance.analysis.coinmarket_start_time import AggregateCoinmarketStartTimeAndAverageVolume

logging.basicConfig(level=logging.INFO)


class Main:
    print("Aggregation started")

    coinmarketcap = CoinmarketCapApi()
    currency_handler = CurrencyHandler()

    ico_handler = ico.main.Main()
    ico_data = ico_handler.get_data()
    print(ico_data)

    AggregateCoinmarketStartTimeAndAverageVolume(coinmarketcap, currency_handler)


Main()
