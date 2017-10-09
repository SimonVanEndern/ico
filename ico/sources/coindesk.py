import csv
import urllib.request
import datetime
import os.path

from ico.initial_coin_offering import ICO


class CoindeskSource:
    csv_import_address = "https://s3.amazonaws.com/media.coindesk.com/ico-tracker-charts/CoinDesk+ICO+Database+-+Blockchain+ICOs.csv"
    now = datetime.datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\saved", "coindesk" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self):
        if os.path.isfile(self.path):
            return
        else:
            urllib.request.urlretrieve(self.csv_import_address, self.path)

    def getIcoData(self, currency_map):
        data = {}
        with open(self.path, "r") as file:
            reader = csv.reader(file)
            icos = list(reader)

            for ico in icos:
                try:
                    date = datetime.datetime.strptime(ico[2], "%m/%d/%Y")
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
