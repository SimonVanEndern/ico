from datetime import datetime
from os import path

from bs4 import BeautifulSoup

from common.parser import Parser


class CoinmarketCapCoinParser(Parser):
    import_address = "https://coinmarketcap.com/coins/views/all/"
    now = datetime.now()
    path_to_save = path.join(path.dirname(__file__) + "\saved",
                             "coinmarketcap-coins" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self):
        super().__init__()

    def get_all_coins(self):
        output = []
        with open(self.path_to_save, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "currencies-all"})
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                # Skip headers
                if index == 0:
                    continue
                currency_name = row.find("td", {"class": "currency-name"}).find("a").text
                output.append(currency_name)

        return output


# run_script = CoinmarketCapCoinParser()
# run_script.get_all_coins()
