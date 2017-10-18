import datetime
import http.client
import json
import os.path

from common.main.json_converter import JsonConverter
from ico_data_crawler.initial_coin_offering import ICO


class CoinmarketCapApi:
    currencies = []

    api_path = "api.coinmarketcap.com"
    api_section1 = "/v1/ticker/"

    now = datetime.datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\saved",
                        "coinmarketcap-tickers" + str(now.year) + str(now.month) + str(now.day) + ".json")
    save_path = os.path.join(os.path.dirname(__file__) + "\saved",
                             "coinmarketcap-data" + str(now.year) + str(now.month) + str(now.day) + ".json")

    def __init__(self):

        if os.path.isfile(self.path):
            with open(self.path, "r") as file:
                self.currencies = json.load(file)
        else:
            conn = http.client.HTTPSConnection(self.api_path)
            conn.request("GET", self.api_section1)
            response = conn.getresponse()
            self.currencies = json.loads(response.read().decode("UTF-8"))

            with open(self.path, "w") as file:
                json.dump(self.currencies, file)

    def get_all_currencies(self):
        return self.currencies

    # returns fullname
    # for multiple = True returns tuple of shortcut and fullname
    def get_currencies(self, multiple=False):
        tickerSymbols = []

        # Get ticker symbol of currencies for requests.
        for currency in self.currencies:
            if multiple:
                tickerSymbols.append([currency["id"], currency["symbol"]])
            else:
                tickerSymbols.append(currency["id"])
        return tickerSymbols

    def getShortnameMap(self, reverse=False):
        shortnames = []
        names = []
        for currency in self.currencies:
            shortnames.append(currency["symbol"])
            names.append(currency["id"])

        if reverse:
            return dict(zip(shortnames, names))
        else:
            return dict(zip(names, shortnames))

    def getIcoData(self):
        data = {}
        for currency in self.currencies:
            data[currency["id"]] = ICO(currency["id"], None, False, None)

        return data

    def get_market_cap(self):
        data = []
        for currency in self.currencies:
            if currency["market_cap_usd"] is not None:
                data.append(int(float(currency["market_cap_usd"])))

        return data

    def get_market_cap_named(self, only_without_market_cap=False):
        data = {}
        for currency in self.currencies:
            if not only_without_market_cap:
                if currency["market_cap_usd"] is not None:
                    data[currency["id"]] = int(float(currency["market_cap_usd"]))
            else:
                if currency["market_cap_usd"] is None:
                    data[currency["id"]] = 0
        return data

    def add_start_date(self, start_dates):
        for currency in self.currencies:
            if currency["id"] in start_dates:
                currency["start_date"] = str(start_dates[currency["id"]])

        return

    def add_highest_market_capitalization(self, highest):
        for currency in self.currencies:
            if currency["id"] in highest:
                currency["highest_market_capitalization"] = highest[currency["id"]]

        return

    def add_volume_average(self, average_volumes):
        for currency in self.currencies:
            if currency["id"] in average_volumes:
                currency["average_volume"] = average_volumes[currency["id"]]

    def save(self):
        if os.path.isfile(self.save_path):
            os.remove(self.save_path)

        with open(self.save_path, "w") as file:
            json.dump(self.currencies, file, cls=JsonConverter)

    def add_ico_data(self, icos):
        for currency in self.currencies:
            if currency["id"] in icos:
                currency["ico"] = icos[currency["id"]]

        print(self.currencies)
