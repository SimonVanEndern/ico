import os

from common.currency import Currency
from globals import GlobalData


class CurrencyHandler:

    all_currencies_with_data = None
    currencies = {}
    data_path = GlobalData.financial_data

    def __init__(self):
        pass

    def get_currency(self, currency):
        if currency not in self.currencies:
            self.load_currency(currency)

        return self.currencies[currency]

    def load_currency(self, currency):
        try:
            self.currencies[currency] = Currency(currency)
        except FileNotFoundError:
            self.currencies[currency] = None

    def get_all_currency_names_where_data_is_available(self, size_limit=math.inf):
        if self.all_currencies_with_data is not None:
            return self.all_currencies_with_data
        else:
            self.all_currencies_with_data = []
            for index, filename in enumerate(os.listdir(self.data_path)):

                self.all_currencies_with_data.append(filename.split(".")[0])

            if len(self.all_currencies_with_data) <= size_limit:
                return self.all_currencies_with_data
            else:
                return self.all_currencies_with_data[:size_limit]
