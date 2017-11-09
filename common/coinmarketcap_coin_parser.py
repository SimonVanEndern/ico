from datetime import datetime
from os import path
from typing import List

from bs4 import BeautifulSoup

from common.currency_handler import CurrencyHandler
from common.parser import Parser


class CoinmarketCapCoinParser(Parser):
    currency_handler: CurrencyHandler = CurrencyHandler.Instance()
    import_address = "https://coinmarketcap.com/coins/views/all/"
    now = datetime.now()
    path_to_save = path.join(path.dirname(__file__) + "\saved",
                             "coinmarketcap-coins" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self, static=False):
        super().__init__()

        if static:
            self.path_to_save = path.join(path.dirname(__file__) + "\saved", "coinmarketcap-coins2017112.html")

    def get_all_coins(self):
        output: List(str) = list()
        with open(self.path_to_save, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "currencies-all"})
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                # Skip headers
                if index == 0:
                    continue
                currency_href = row.find("td", {"class": "currency-name"}).find("a")['href']
                splits = currency_href.split("/")
                currency_name = splits[len(splits) - 2]
                output.append(currency_name)

        all_currencies = self.currency_handler.get_all_currency_names()
        to_remove = list()
        for currency in output:
            if currency not in all_currencies:
                to_remove.append(currency)

        for currency in to_remove:
            output.remove(currency)

        return output

# run_script = CoinmarketCapCoinParser()
# run_script.get_all_coins()
