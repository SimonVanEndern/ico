import csv
import datetime

from global_data import GlobalData
from ico.initial_coin_offering import ICO


class IcobazaarSource:
    baseAddress = GlobalData.ico_data_path

    filename = "\icobazaar-2017-09-26-11-16uhr.csv"

    def __init__(self):
        with open(self.baseAddress + self.filename) as file:
            reader = csv.reader(file, delimiter=";")
            self.icos = list(reader)

    def getIcoData(self, currency_map):
        data = {}
        for idx, ico in enumerate(self.icos):
            if idx == 0:
                continue

            date = datetime.datetime.strptime(ico[3], "%d.%m.%Y")
            ico = ICO(ico[0], date, True, ico[4])
            if ico.name.lower() in currency_map:
                data[currency_map[ico.name.lower()]] = ico
                # print(ico.name.lower() + " Found")
                # print(currency_map[ico.name.lower()])
            else:
                data[ico.name] = ico
                # print(ico.name + " Not found in map")

        return data
