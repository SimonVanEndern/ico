from datetime import datetime
from typing import Dict

from common.currency import Currency
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData


class WithinCurrencies:
    def __init__(self, start_date: datetime = None):
        self.start_date: datetime = start_date
        self.currency_handler: CurrencyHandler = CurrencyHandler.Instance()
        self.data: Dict[str, CurrencyStatisticalData] = dict()

    def get_and_export_data(self, currencies: list) -> Dict[str, CurrencyStatisticalData]:
        for index, currency in enumerate(currencies):

            handle_on_currency: Currency = self.currency_handler.get_currency(currency, date_limit=self.start_date)
            if handle_on_currency is None:
                continue
            data = handle_on_currency.get_statistical_data()
            if data is not None:
                self.data[currency] = data

        return self.data
