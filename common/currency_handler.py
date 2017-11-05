import json
import logging
import math
import os
import time
from typing import Dict

import requests

from common.coinmarketCapApi import CoinmarketCapApi
from common.currency import Currency
from csv_strings import CSVStrings
from global_data import GlobalData


class CurrencyHandler:
    def __init__(self, static=False):
        self.currencies: Dict(str, Dict[str, 'Currency']) = dict()
        self.all_currencies_with_data = None

        self.logger = logging.getLogger(self.__class__.__name__)

        self.coinmarketcapAPI: CoinmarketCapApi = CoinmarketCapApi(static=static)

        self.data_path: str = GlobalData.financial_data_path

        self.basic_currency_data = self.load_basic_currency_data()
        self.all_currency_names = self.load_all_currency_names()

    def get_currency(self, currency, date_limit=None) -> Currency:
        if currency not in self.currencies:
            self.load_currency(currency, date_limit)
        else:
            if date_limit not in self.currencies[currency]:
                self.load_currency(currency, date_limit)

        return self.currencies[currency][str(date_limit)]

    def load_currency(self, currency, date_limit=None) -> None:
        if currency not in self.currencies:
            self.currencies[currency]: dict = dict()
        try:
            self.currencies[currency][str(date_limit)] = Currency(currency, date_limit=date_limit)
        except FileNotFoundError:
            logging.warning("Currency {} not found!".format(currency))
            self.currencies[currency][str(date_limit)] = None

    def get_all_currency_names_where_data_is_available(self, size_limit=math.inf) -> list:
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

    def get_financial_series_start_date_of_all_currencies(self, limit=math.inf):
        output = list()
        for key, value in sorted(self.currencies.items()):
            value[str(None)].get_statistical_data()
            output.append(value[str(None)].statistical_data.first_date)

            if len(output) > limit:
                break

        return output

    def load_basic_currency_data(self) -> dict:
        filename: str = "basic-currency-data.json"
        file_path: str = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)
        if os.path.isfile(file_path):
            with open(file_path) as file:
                return json.load(file)

        return dict()

    def save_basic_currency_data(self) -> None:
        filename: str = "basic-currency-data.json"
        file_path: str = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

        if os.path.isfile(file_path):
            os.remove(file_path)

        with open(file_path, "w") as file:
            json.dump(self.basic_currency_data, file)

    def save_all_currency_names_data(self) -> None:
        filename: str = "all-currency-names.json"
        file_path: str = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

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

    def load_all_currencies(self) -> None:
        for currency in self.get_all_currency_names_where_data_is_available():
            self.load_currency(currency)

    def load_all_currency_names(self) -> dict:
        filename: str = "basic-currency-data.json"
        file_path: str = os.path.join(GlobalData.CURRENCY_HANDLER_PATH, filename)

        if os.path.isfile(file_path):
            with open(file_path) as file:
                return json.load(file)

        return dict()

    def get_all_currency_names(self) -> list:
        currencies: list = self.get_all_currency_names_where_data_is_available()

        additional: list = self.coinmarketcapAPI.get_all_currencies()

        for currency in additional:
            if currency["id"] in currencies:
                pass
            else:
                currencies.append(currency["id"])

        self.all_currency_names = currencies
        self.save_all_currency_names_data()
        return self.all_currency_names
