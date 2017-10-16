import logging
import os

from common.currency_handler import CurrencyHandler
from finance.raw_data.coinmarketcap_importer import CoinMarketCapGraphAPIImporter
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class RawDataImporter:
    def __init__(self):
        self.currency_handler = CurrencyHandler()
        self.coinmarketcap_importer = CoinMarketCapGraphAPIImporter()

        self.last_timestamp = GlobalData.last_date_for_download

    def download_all_data(self):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available()

        if os.path.isfile(
                os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, "ready" + str(self.last_timestamp))):
            logging.info(
                "{}: All currencies until {} already downloaded".format(self.__class__.__name__, self.last_timestamp))

        for currency in currencies:
            logging.info("{}:Start - Downloading currency:{}".format(self.__class__.__name__, currency))
            self.coinmarketcap_importer.request_currency(currency, self.last_timestamp)
            logging.info("{}:End - Downloading currency:{}".format(self.__class__.__name__, currency))

        # Mark currency download until last_date as finished
        open(os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, "ready" + str(self.last_timestamp))).close()
        logging.info(
            "{}: Finished downloading currencies until {}".format(self.__class__.__name__, self.last_timestamp))


RawDataImporter().download_all_data()
