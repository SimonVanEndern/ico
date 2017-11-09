import logging
import os

from common.currency_handler import CurrencyHandler
from finance_data_import.raw_data.coinmarketcap_importer import CoinMarketCapGraphAPIImporter
from global_data import GlobalData


class RawDataImporter:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.currency_handler = CurrencyHandler.Instance()
        self.coinmarketcap_importer = CoinMarketCapGraphAPIImporter()

        self.last_timestamp = GlobalData.last_date_for_download

    def download_all_data(self):
        currencies = self.currency_handler.get_all_currency_names()

        if os.path.isfile(
                os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, "ready" + str(self.last_timestamp))):
            self.logger.info("All currencies until {} already downloaded".format(self.last_timestamp))

        for currency in currencies:
            self.logger.info("Start - Downloading currency:{}".format(currency))
            self.coinmarketcap_importer.request_currency(currency, self.last_timestamp)
            self.logger.info("End - Downloading currency:{}".format(currency))

        # Mark currency download until last_date as finished
        open(os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, "ready" + str(self.last_timestamp)), "w").close()
        self.logger.info("Finished downloading currencies until {}".format(self.last_timestamp))
