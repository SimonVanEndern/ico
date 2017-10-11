import os

import math

from common.currency import Currency
from globals import GlobalData


class CurrencyHandler:

    all_currencies_with_data = None
    currencies = {}
    data_path = GlobalData.financial_data

    def __init__(self):
        pass

    def get_currency(self, currency, date_limit=None):
        if currency not in self.currencies:
            self.load_currency(currency, date_limit)
        else:
            if date_limit not in self.currencies[currency]:
                self.load_currency(currency, date_limit)

        return self.currencies[currency][str(date_limit)]

    def load_currency(self, currency, date_limit=None):
        try:
            self.currencies[currency] = {str(date_limit): Currency(currency, date_limit=date_limit)}
        except FileNotFoundError:
            self.currencies[currency] = {str(date_limit): None}

    def get_all_currency_names_where_data_is_available(self, size_limit=math.inf):
        if self.all_currencies_with_data is not None:
            if len(self.all_currencies_with_data) <= size_limit:
                return self.all_currencies_with_data
            else:
                return self.all_currencies_with_data[:size_limit]

        else:
            self.all_currencies_with_data = []
            for index, filename in enumerate(os.listdir(self.data_path)):

                self.all_currencies_with_data.append(filename.split(".")[0])

            if len(self.all_currencies_with_data) <= size_limit:
                return self.all_currencies_with_data
            else:
                return self.all_currencies_with_data[:size_limit]
