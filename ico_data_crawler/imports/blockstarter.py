import http.client
import logging
import os.path
from datetime import datetime

import requests
from bs4 import BeautifulSoup

from ico_data_crawler.imports.importer import Importer
from ico_data_crawler.initial_coin_offering import ICO

logging.basicConfig(level=logging.DEBUG)

http.client.HTTPSConnection.debuglevel = 1


class BlockstarterSource(Importer):
    html_import_address = "http://blockstarter.co/icodb/"

    def __init__(self):
        super().__init__()
        self.path = os.path.join(os.path.dirname(__file__) + "\saved",
                                 "blockstarter" + super().get_filename_date() + ".html")
        self.data = {}
        if os.path.isfile(self.path):
            return
        else:
            request = requests.get(self.html_import_address)
            with open(self.path, "w") as file:
                file.write(request.text)

    def getIcoData(self):
        data = {}
        with open(self.path, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            currencies = soup.find("div", {"class": "products-panel"}).find_all("div", {"class": "product"})
            for currency in currencies:
                name = currency.find("div", {"class": "title"}).text.strip()
                money = currency.find("div", {"class": "amounts"}).text
                money = money[0:money.index("Read")]
                date = currency.find("div", {"class": "panel"}).find_all("div", {"class": "val"})[1].text

                if money != "":
                    ico = ICO(name, None, True, money)
                else:
                    ico = ICO(name, None, False, "")

                if date == "" or date == "n/a":
                    ico.close_date = None
                else:
                    ico.close_date = datetime.strptime(date, '%m.%d.%Y')

                data[name] = ico

        return data
