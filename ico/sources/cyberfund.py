import datetime
import http.client
import logging
import os.path
import re
from datetime import timedelta

import requests
from bs4 import BeautifulSoup

from ico.initial_coin_offering import ICO

logging.basicConfig(level=logging.DEBUG)

http.client.HTTPSConnection.debuglevel = 1


class CyberfundSource:
    html_import_address = "https://cyber.fund/radar"
    now = datetime.datetime.now()
    # path = os.path.join(os.path.dirname(__file__) + "\saved",
    #                     "cyberfund" + str(now.year) + str(now.month) + str(now.day) + ".html")
    path = os.path.join(os.path.dirname(__file__) + "\saved",
                         "cyberfund" + "2017102" + ".html")

    def __init__(self):
        self.data = {}
        if os.path.isfile(self.path):
            return
        else:
            request = requests.get(self.html_import_address)
            with open(self.path, "w") as file:
                file.write(request.text)

    def getIcoData(self, currency_map):
        data = {}
        with open(self.path, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            currencies = soup.find_all("div", {"class": "card"})
            for currency in currencies:
                name = currency.find("div", {"class": "card-title"}).text.strip()

                date = currency.find("div", {"class": "card-content"}).find("div", {"class": "center-align"})
                if date is not None:
                    date = date.text.strip()
                    numbers = re.findall(r'\d+', date)
                    if int(numbers[0]) != 17441:
                        date = datetime.datetime.now() - timedelta(days=int(numbers[0]))
                    else:
                        date = None

                money = currency.find("div", {"class": "card-content"}).find("strong")
                if money is not None:
                    money = money.text.replace("\n", "").replace("\t", "").replace("raised", "").strip()
                    if "cap" in money:
                        money = ""

                if money != "":
                    ico = ICO(name, None, True, money)
                else:
                    ico = ICO(name, None, False, "")

                ico.date = date

                if name.lower() in currency_map:
                    data[currency_map[name.lower()]] = ico
                else:
                    data[name.lower()] = ico

        return data


CyberfundSource().getIcoData({})
