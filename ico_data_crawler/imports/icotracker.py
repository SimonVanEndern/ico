import datetime
import http.client
import logging
import os.path

from bs4 import BeautifulSoup

from global_data import GlobalData

logging.basicConfig(level=logging.DEBUG)

http.client.HTTPSConnection.debuglevel = 1

from ico_data_crawler.initial_coin_offering import ICO


class IcotrackerSource:
    filename = "Actual crowdsales - ICO Tracker-2017-09-28.html"
    baseAddress = GlobalData.ico_data_path
    path = os.path.join(baseAddress, filename)

    def __init__(self):
        return

    def getIcoData(self):
        data = {}
        with open(self.path, "r", encoding='UTF-8') as file:
            soup = BeautifulSoup(file, "html.parser")
            all_currencies = soup.find_all("div", {"class": "card-block"})
            for currency in all_currencies:

                name = currency.find('a', {"title": "Project Details"}).text
                divs = currency.find_all('div', {"class": "cp-row-sm"})
                try:
                    date = divs[4].find('span', {"class": "text-black"}).text
                    try:
                        date = date.split("-")[1].strip()
                        try:
                            date = datetime.datetime.strptime(date, "%d/%m/%Y")
                        except ValueError:
                            print("Format Error: " + str(date))
                    except IndexError:
                        date = None
                        print("Indexerror: " + str(date))
                except IndexError:
                    # Scam:
                    date = None

                try:
                    money = divs[5].find_all('span', {"class": "text-black"})[1].text
                except IndexError:
                    money = None

                ico = ICO(name, date, True, money)
                if ico.raised_money == "Ƀ0":
                    ico.funds = False
                data[ico.name] = ico

        return data
