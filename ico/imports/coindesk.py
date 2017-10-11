import csv
from datetime import datetime
import logging
import os.path
import urllib.request

from ico.initial_coin_offering import ICO


class CoindeskSource:
    csv_import_address = "https://s3.amazonaws.com/media.coindesk.com/ico-tracker-charts/CoinDesk+ICO+Database+-+Blockchain+ICOs.csv"
    now = datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\saved",
                        "coindesk" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self):
        logging.info("Starting up {} with path {}".format(self.__class__.__name__, self.path))
        if os.path.isfile(self.path):
            return
        else:
            urllib.request.urlretrieve(self.csv_import_address, self.path)

    def get_ico_data(self, currency_map):
        if self.now > datetime.strptime("29.09.2017", "%d.%m.%Y"):
            return self.get_ico_data_after_september_2017(currency_map)

        data = {}
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            icos = list(reader)

            for index, ico in enumerate(icos):
                if index == 0:
                    continue

                try:
                    date = datetime.strptime(ico[2], "%m/%d/%Y")
                except ValueError:
                    date = None
                ico = ICO(ico[0], date, True, ico[6])
                if ico.name.lower() in currency_map:
                    data[currency_map[ico.name.lower()]] = ico
                    # print(ico.name.lower() + " Found")
                    # print(currency_map[ico.name.lower()])
                else:
                    data[ico.name] = ico
                    # print(ico.name + " Not found in map")

        return data

    def get_ico_data_after_september_2017(self, currency_map):
        data = {}
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            icos = list(reader)

            for index, ico in enumerate(icos):
                if index == 0:
                    continue

                try:
                    date = datetime.strptime(ico[1], "%m/%d/%Y")
                except ValueError:
                    date = None
                ico = ICO(ico[0], date, True, ico[4])
                if ico.name.lower() in currency_map:
                    data[currency_map[ico.name.lower()]] = ico
                else:
                    data[ico.name] = ico

        return data
