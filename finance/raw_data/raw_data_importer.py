import logging

from common.currency_handler import CurrencyHandler
from finance.raw_data.coinmarketcap_importer import CoinmarketcapImportFinanceData


logging.basicConfig(level=logging.INFO)


class RawDataImporter:

    def __init__(self):
        self.currency_handler = CurrencyHandler()
        self.coinmarketcap_importer = CoinmarketcapImportFinanceData()

    def download_all_data(self):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available()

        for currency in currencies:
            logging.info("{}:Start - Downloading currency:{}".format(self.__class__.__name__, currency))
            self.coinmarketcap_importer.request_currency(currency)
            logging.info("{}:End - Downloading currency:{}".format(self.__class__.__name__, currency))


# RawDataImporter().download_all_data()
