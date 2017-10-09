import datetime
import http.client
import logging
import os.path

import requests
from bs4 import BeautifulSoup

from ico.initial_coin_offering import ICO

logging.basicConfig(level=logging.DEBUG)

http.client.HTTPSConnection.debuglevel = 1


class CoinscheduleSource:
    html_import_address = "https://www.coinschedule.com/icos.php"
    now = datetime.datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\saved",
                        "coinschedule" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self):
        if os.path.isfile(self.path):
            return
        else:
            # urllib.request.urlretrieve(self.html_import_address, self.path)
            request = requests.get(self.html_import_address)
            with open(self.path, "w") as file:
                file.write(request.content.decode("UTF-8"))
                # conn = http.client.HTTPSConnection("coinschedule.com")
                # conn.request("GET", "/icos.php")
                # response = conn.getresponse()
                # print(response.read().decode("UTF-8"))

    def getIcoData(self, currency_map):
        data = {}
        with open(self.path, "r", encoding='UTF-8') as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "tbl_icos"})
            for idx, row in enumerate(table.find_all("tr")):
                if idx == 0:
                    continue
                infos = row.find_all("td")
                name = infos[0].text
                end_date = infos[3].text
                end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")
                money = infos[4].text

                ico = ICO(name, end_date, True, money)
                if name.lower() in currency_map:
                    data[currency_map[name.lower()]] = ico
                else:
                    data[name.lower()] = ico

                # print(ico)

        return data


# CoinscheduleSource().getIcoData({})
