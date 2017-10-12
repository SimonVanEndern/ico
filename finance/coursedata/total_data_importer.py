import logging

from common.currency_handler import CurrencyHandler
from finance.coursedata.coinmarketcap_importer import CoinmarketcapImportFinanceData


logging.basicConfig(level=logging.INFO)


class TotalDataImporter:

    def __init__(self):
        self.currency_handler = CurrencyHandler()
        self.coinmarketcap_importer = CoinmarketcapImportFinanceData()

    def download_all_data(self):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available()

        self.coinmarketcap_importer.request_currency("bitcoin")

        for currency in currencies:
            logging.info("{}:Start - Downloading currency:{}".format(self.__class__.__name__, currency))
            self.coinmarketcap_importer.request_currency(currency)


TotalDataImporter().download_all_data()
