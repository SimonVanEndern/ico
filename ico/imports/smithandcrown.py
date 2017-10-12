import datetime
import http.client
import logging
import os.path
import urllib.request

import requests
from bs4 import BeautifulSoup

from ico.initial_coin_offering import ICO

logging.basicConfig(level=logging.DEBUG)

http.client.HTTPSConnection.debuglevel = 1


class SmithandcrownSource:
    html_import_address = "https://www.smithandcrown.com/icos/"
    now = datetime.datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\saved",
                        "smithandcrown" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self):
        self.data = {}
        if os.path.isfile(self.path):
            return
        else:
            urllib.request.urlretrieve(self.html_import_address, self.path)

    def getIcoData(self):
        with open(self.path, "r") as file:
            soup = BeautifulSoup(file, "html.parser")
            # TODO check whether we do data on ongoing ICOs as well
            # table_ongoing = soup.find("table", {"id": "icos-ongoing"})
            table_recent = soup.find("table", {"id": "icos-recent"})
            # self.data = self.iterate_table(table_ongoing, currency_map)
            self.data.update(self.iterate_table(table_recent))

        return self.data

    def iterate_table(self, table):
        data = {}
        for idx, row in enumerate(table.find_all("tr")):
            if idx == 0:
                continue
            infos = row.find_all("td")
            name = infos[0].find("span").text
            name = name[0: name.index("(")].rstrip()
            end_date = infos[5].text.strip()
            end_date = datetime.datetime.strptime(end_date, "%b %d, %Y")
            money = infos[6].text
            if "$" in money:
                ico = ICO(name, end_date, True, money)
            else:
                ico = ICO(name, end_date, False, "")
            data[name] = ico

        return data
