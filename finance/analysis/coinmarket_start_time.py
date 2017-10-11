import csv
import os.path
from datetime import datetime

import scipy

from common.currency_handler import CurrencyHandler
from globals import GlobalData


class AggregateCoinmarketStartTime:
    data_path = GlobalData.financial_data
    start_time_data = []
    currency_handler = CurrencyHandler()

    highest_market_cap_data = {}

    now = datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\\aggregated",
                        "start_date" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self, coinmarketcap):
        self.coinmarketcap = coinmarketcap
        if os.path.isfile(self.path):
            with open(self.path, "r") as file:
                reader = csv.reader(file)
                self.start_time_data = list(reader)
            return
        else:
            self.aggregate_start_time_data()
            self.highest_market_cap_data = self.get_highest_market_cap()
            self.coinmarketcap.add_highest_market_capitalization(self.highest_market_cap_data)
            self.coinmarketcap.save()

    def aggregate_start_time_data(self):
        json_currencies = {}
        json_currencies_volume = {}
        currencies = []
        start_time = []
        for filename in os.listdir(self.data_path):
            with open(os.path.join(self.data_path, filename), "r") as file:
                reader = csv.reader(file)
                icos = list(reader)

                volume = self.calculate_average_volume(icos)

                beginning_date = datetime.fromtimestamp(int(icos[2][0]) / 1e3)
                start_time.append(beginning_date)
                currencies.append(filename.split(".")[0])
                json_currencies[filename.split(".")[0]] = beginning_date
                json_currencies_volume[filename.split(".")[0]] = volume

        self.start_time_data = zip(currencies, start_time)
        self.coinmarketcap.add_start_date(json_currencies)
        self.coinmarketcap.add_volume_average(json_currencies_volume)
        self.coinmarketcap.save()
        with open(self.path, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow(["Currency", "Start-Date"])
            for row in self.start_time_data:
                writer.writerow(row)

    def get_start_time_data(self):
        return self.start_time_data

    def get_highest_market_cap(self):
        json_output = {}
        currencies = self.coinmarketcap.get_currencies()
        for index, currency in enumerate(currencies):
            try:
                result = self.currency_handler.get_currency(currency)
                if result is not None:
                    data = result.get_volume_financial_data()
                else:
                    json_output[currency] = None
                    continue
                sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                highest = sorted_data[0]
                json_output[currency] = highest[1]
            except FileNotFoundError:
                json_output[currency] = None

        return json_output

    def calculate_average_volume(self, data):
        timestamp, usd, btc, volume, market_cap = zip(*data)
        volume = list(volume)
        volume.pop(0)
        volume = list(map(int, volume))
        return scipy.mean(volume)

