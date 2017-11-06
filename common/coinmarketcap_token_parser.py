from collections import Counter
from datetime import datetime
from os import path

import matplotlib.pyplot as plt
import pandas
from bs4 import BeautifulSoup

from common.currency_handler import CurrencyHandler
from common.parser import Parser


class CoinmarketCapTokenParser(Parser):
    currency_handler: CurrencyHandler = CurrencyHandler()
    import_address = "https://coinmarketcap.com/tokens/views/all/"
    now = datetime.now()
    path_to_save = path.join(path.dirname(__file__) + "\saved",
                             "coinmarketcap-tokens" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self, static=False):
        super().__init__()

        if static:
            self.path_to_save = path.join(path.dirname(__file__) + "\saved", "coinmarketcap-tokens2017112.html")

    def get_all_tokens(self):
        output: list = list()
        with open(self.path_to_save, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "assets-all"})
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                # Skip headers
                if index == 0:
                    continue
                currency_href = row.find("td", {"class": "currency-name"}).find("a")['href']
                splits = currency_href.split("/")
                currency_name = splits[len(splits) - 2]
                platform_name = row.find("td", {"class": "platform-name"}).find("a").text
                output.append({"currency": currency_name, "platform": platform_name})

        all_currencies = self.currency_handler.get_all_currency_names()
        to_remove = list()
        for currency in output:
            if currency["currency"] not in all_currencies:
                to_remove.append(currency)

        for currency in to_remove:
            output.remove(currency)

        return output

    def get_platform_statistics(self):
        tokens = self.get_all_tokens()
        tokens = list(map(lambda x: x["platform"], tokens))

        token_counts = Counter(tokens)

        df = pandas.DataFrame.from_dict(token_counts, orient='index')
        df.plot(kind='bar')

        print("Figure 01: ")
        plt.show()

        return len(token_counts)

# run_script = CoinmarketCapTokenParser()
# run_script.get_platform_statistics()
