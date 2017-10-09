from datetime import datetime
from os import path

from bs4 import BeautifulSoup

from common.parser import Parser
import numpy
import matplotlib.pyplot as plt
import pandas
from collections import Counter


class CoinmarketCapTokenParser(Parser):
    import_address = "https://coinmarketcap.com/tokens/views/all/"
    now = datetime.now()
    path_to_save = path.join(path.dirname(__file__) + "\saved",
                             "coinmarketcap-tokens" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self):
        super().__init__()

    def get_all_tokens(self):
        output = []
        with open(self.path_to_save, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "assets-all"})
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                # Skip headers
                if index == 0:
                    continue
                currency_name = row.find("td", {"class": "currency-name"}).find("a").text
                platform_name = row.find("td", {"class": "platform-name"}).find("a").text
                output.append({"currency": currency_name, "platform": platform_name})

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
