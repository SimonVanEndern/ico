import json
import logging
import math
import os
import time

import requests

from common.coinmarketCapApi import CoinmarketCapApi
from common.currency import Currency
from csv_strings import CSVStrings
from global_data import GlobalData


class CurrencyHandler:
    def __init__(self):
        self.currencies = dict()
        self.all_currencies_with_data = None

        self.logger = logging.getLogger(self.__class__.__name__)

        self.coinmarketcapAPI = CoinmarketCapApi()

        self.data_path = GlobalData.financial_data_path

        self.basic_currency_data = self.load_basic_currency_data()

        self.all_currency_names = self.load_all_currency_names()

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
                if not os.path.isdir(os.path.join(self.data_path, filename)):
                    self.all_currencies_with_data.append(filename.split(".")[0])

            if len(self.all_currencies_with_data) <= size_limit:
                return self.all_currencies_with_data
            else:
                return self.all_currencies_with_data[:size_limit]

    def get_basic_currency_data(self, currency):
        if currency in self.basic_currency_data:
            return self.basic_currency_data[currency]
        else:
            time.sleep(1)
            path = ("https://" + GlobalData.coin_market_cap_graph_api_url + "/currencies/{}/").format(currency)
            response = requests.request("GET", path)

            if response.status_code == 404:
                self.logger.info("Currency {} not listed anymore".format(currency))
                self.basic_currency_data[currency] = None
            else:
                data = json.loads(response.text)
                datapoints = data[CSVStrings.price_usd_string]

                self.basic_currency_data[currency] = {"start_date": datapoints[0][0]}
            self.save_basic_currency_data()
            return self.basic_currency_data[currency]

    def get_financial_series_start_date(self, currency):
        return self.currencies[currency].get_beginning_date()

    def get_financial_series_start_date_of_all_currencies(self):
        output = list()
        for key, value in sorted(self.currencies.items()):
            output.append(value[str(None)].get_beginning_date())

        return output

    def load_basic_currency_data(self):
        filename = "basic-currency-data.json"
        file_path = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)
        if os.path.isfile(file_path):
            with open(file_path) as file:
                return json.load(file)

        return dict()

    def save_basic_currency_data(self):
        filename = "basic-currency-data.json"
        file_path = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

        with open(file_path, "w") as file:
            json.dump(self.basic_currency_data, file)

    def save_all_currency_names_data(self):
        filename = "all-currency-names.json"
        file_path = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

        with open(file_path, "w") as file:
            json.dump(self.all_currency_names, file)

    def load_ico_data(self):
        pass
        # TODO: implement

    def add_ico_data(self, icos):
        for currency in self.currencies:
            if currency["id"] in icos:
                currency["ico"] = icos[currency["id"]]

    def load_all_currencies(self):
        for currency in self.get_all_currency_names_where_data_is_available():
            self.load_currency(currency)

    def load_all_currency_names(self):
        filename = "basic-currency-data.json"
        file_path = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

        if os.path.isfile(file_path):
            with open(file_path) as file:
                return json.load(file)

        return dict()

    def get_all_currency_names(self):
        currencies = self.get_all_currency_names_where_data_is_available()

        additional = self.coinmarketcapAPI.get_all_currencies()

        for currency in additional:
            if currency["id"] in currencies:
                pass
            else:
                currencies.append(currency["id"])

        self.all_currency_names = currencies
        return self.all_currency_names
