import logging

from common.currency_handler import CurrencyHandler
from finance.compressed_raw_data.currency_compressor import CurrencyCompressor

logging.basicConfig(level=logging.INFO)


class SimplifyRawData:
    def __init__(self):
        self.currency_handler = CurrencyHandler()

    # Main
    def compress_data(self, last_time):
        logging.info("{} Compressing data for all currencies".format(self.__class__.__name__))

        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            CurrencyCompressor(currency, last_time)
