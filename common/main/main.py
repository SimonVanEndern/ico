import logging

import ico_data_crawler.main
from common.coinmarketCapApi import CoinmarketCapApi
from common.currency_handler import CurrencyHandler
from finance_data_import.main import MainDataImporter

logging.basicConfig(level=logging.INFO)


class Main:
    def __init__(self):
        # Run financial data (coinmarketcap) importer / aggregator
        MainDataImporter().run()

        # Run ICO start and funding data importer
        ico_handler = ico_data_crawler.main.Main()

        ico_data = ico_handler.get_data()
        self.currency_handler = CurrencyHandler()
        self.currency_handler.add_ico_data(ico_data)
        logging.info("common:main:main - Aggregation started")

        coinmarketcap = CoinmarketCapApi()

        # print(ico_data)
        # coinmarketcap.add_ico_data(ico_data)
        coinmarketcap.save()

    def test(self):
        print(self.currency_handler.get_currency("bitcoin"))


    # AggregateCoinmarketStartTimeAndAverageVolume(coinmarketcap, currency_handler)


Main().test()
