import csv
import os
from datetime import datetime
from typing import Dict

from common.currency import Currency
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from global_data import GlobalData


class WithinCurrencies:
    def __init__(self, start_date: datetime = None):
        self.start_date: datetime = start_date
        self.currency_handler: CurrencyHandler = CurrencyHandler(static=True)
        self.data: Dict[str, CurrencyStatisticalData] = dict()

    def get_and_export_data(self) -> Dict[str, CurrencyStatisticalData]:
        for index, currency in enumerate(self.currency_handler.get_all_currency_names()):

            handle_on_currency: Currency = self.currency_handler.get_currency(currency, date_limit=self.start_date)
            self.data[currency] = handle_on_currency.get_statistical_data()

        return self.data


# WithinCurrencies().get_and_export_data()
