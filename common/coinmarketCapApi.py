import datetime
import http.client
import json
import os.path
from typing import Dict, List, Tuple

from common.main.json_converter import JsonConverter


class CoinmarketCapApi:
    currencies: list = list()

    api_path: str = "api.coinmarketcap.com"
    api_section1: str = "/v1/ticker/?limit=0"

    now: datetime = datetime.datetime.now()

    if not os.path.isdir(os.path.join(os.path.dirname(__file__), "saved")):
        os.mkdir(os.path.join(os.path.dirname(__file__), "saved"))

    save_path: str = os.path.join(os.path.dirname(__file__), "saved",
                                  "coinmarketcap-tickers" + str(now.year) + str(now.month) + str(now.day) + ".json")

    def __init__(self, static=False):
        dict_currencies: dict = dict()

        if static:
            self.save_path = os.path.join(os.path.dirname(__file__), "saved", "coinmarketcap-tickers2017115.json")

        if os.path.isfile(self.save_path):
            with open(self.save_path, "r") as file:
                self.currencies: list = json.load(file)
        else:
            conn = http.client.HTTPSConnection(self.api_path)
            conn.request("GET", self.api_section1)
            response = conn.getresponse()
            self.currencies: List[dict] = json.loads(response.read().decode("UTF-8"))

            self.save()

        for currency in self.currencies:
            dict_currencies[currency["id"]] = currency

        for currency in dict_currencies:
            self.currencies.append(dict_currencies[currency])

    def get_all_currencies(self) -> List[dict]:
        """
        dict attributes:
        - id
        - name
        - symbol
        - price_usd
        ...

        :return: A list of all known currencies
        """
        return self.currencies

    def get_currency_ticker_symbols(self) -> List[str]:
        """

        :return: 'id' of currency e.g. 'bitcoin' or 'ethereum'
        """
        return list(map(lambda x: x["id"], self.currencies))

    def get_currency_ticker_symbols_fullname_tuple(self) -> List[Tuple[str, str]]:
        """
        id: see get_currency_ticker_symbols
        symbol: 3 capital letters e.g. BTC
        :return: Tuple of id and symbol
        """
        return list(map(lambda x: (x["id"], x["symbol"]), self.currencies))

    def getIdToSymbolMapping(self, reverse=False) -> dict:
        symbols: list = list()
        id: list = list()
        for currency in self.currencies:
            symbols.append(currency["symbol"])
            id.append(currency["id"])

        if reverse:
            return dict(zip(symbols, id))
        else:
            return dict(zip(id, symbols))

    def get_market_cap_named(self, only_without_market_cap=False):
        data: Dict[str, int] = dict()
        for currency in self.currencies:
            if not only_without_market_cap:
                if currency["market_cap_usd"] is not None:
                    data[currency["id"]] = int(float(currency["market_cap_usd"]))
            else:
                if currency["market_cap_usd"] is None:
                    data[currency["id"]] = 0
        return data

    def save(self):
        """
        Saving the data. Usually not necessary, as data after init is not changed any more
        :return:
        """
        if os.path.isfile(self.save_path):
            os.remove(self.save_path)

        with open(self.save_path, "w") as file:
            json.dump(self.currencies, file, cls=JsonConverter)
