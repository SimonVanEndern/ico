import logging

from common.currency_handler import CurrencyHandler
from finance_data_import.aggregated_data.currency_aggregator import CurrencyAggregator

# logging.basicConfig(level=logging.INFO)


class ReduceSimplifiedData:
    def __init__(self):
        self.currency_handler = CurrencyHandler()

    def aggregate_compressed_data(self, last_time):
        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            if currency == "cabbage":
                x = 4
                pass
            CurrencyAggregator(currency, last_time).run()
