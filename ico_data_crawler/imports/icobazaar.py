import csv
import datetime

from global_data import GlobalData
from ico_data_crawler.initial_coin_offering import ICO


class IcobazaarSource:
    baseAddress = GlobalData.ico_data_path

    filename = "\icobazaar-2017-09-26-11-16uhr.csv"

    def __init__(self):
        with open(self.baseAddress + self.filename) as file:
            reader = csv.reader(file, delimiter=";")
            self.icos = list(reader)

    def getIcoData(self):
        data = {}
        for idx, ico in enumerate(self.icos):
            if idx == 0:
                continue

            date = datetime.datetime.strptime(ico[3], "%d.%m.%Y")
            ico = ICO(ico[0], date, True, ico[4])
            data[ico.name] = ico

        return data
