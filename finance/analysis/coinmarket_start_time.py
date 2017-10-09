import csv
import os.path
from datetime import datetime

import common.coinmarketCapApi
import common.currency


class AggregateCoinmarketStartTime:
    example_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-09-28"
    start_time_data = []
    coinmarketcap = common.coinmarketCapApi.CoinmarketCapApi()
    currency_provider = common.currency.Currency()
    highest_market_cap_data = {}

    now = datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\\aggregated",
                        "start_date" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self):
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
        currencies = []
        start_time = []
        for filename in os.listdir(self.example_path):
            with open(os.path.join(self.example_path, filename), "r") as file:
                reader = csv.reader(file)
                icos = list(reader)

                beginning_date = datetime.fromtimestamp(int(icos[2][0]) / 1e3)
                start_time.append(beginning_date)
                currencies.append(filename.split(".")[0])
                json_currencies[filename.split(".")[0]] = beginning_date

        self.start_time_data = zip(currencies, start_time)
        self.coinmarketcap.add_start_date(json_currencies)
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
                data = self.currency_provider.get_volume_financial_data(currency)
                sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
                highest = sorted_data[0]
                json_output[currency] = highest[1]
            except FileNotFoundError:
                json_output[currency] = None

        return json_output


run_script = AggregateCoinmarketStartTime()
# run_script.get_highest_market_cap()
