import csv
import os.path
from datetime import datetime

import scipy

from globals import GlobalData


def calculate_average_volume(data):
    timestamp, usd, btc, volume, market_cap = zip(*data)
    volume = list(volume)
    volume.pop(0)
    volume = list(map(int, volume))
    return scipy.mean(volume)


class AggregateCoinmarketStartTimeAndAverageVolume:
    data_path = GlobalData.financial_data
    start_time_data = []

    highest_market_cap_data = {}

    now = datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\\aggregated",
                        "start_date" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self, coinmarketcap, currency_handler):
        self.currency_handler = currency_handler
        self.coinmarketcap = coinmarketcap
        if os.path.isfile(self.path):
            with open(self.path, "r") as file:
                reader = csv.reader(file)
                self.start_time_data = list(reader)
            return
        else:
            self.aggregate_start_time_data_and_average_volume()
            self.highest_market_cap_data = self.get_highest_market_cap()
            self.coinmarketcap.add_highest_market_capitalization(self.highest_market_cap_data)
            self.coinmarketcap.save()

    def aggregate_start_time_data_and_average_volume(self):
        json_currencies = {}
        json_currencies_volume = {}
        currencies = []
        start_time = []
        results = self.currency_handler.get_all_currency_names_where_data_is_available()
        for filename in results:
            currency = self.currency_handler.get_currency(filename)

            volume = currency.calculate_average_volume()

            beginning_date = datetime.fromtimestamp(currency.get_beginning_date() / 1e3)
            start_time.append(beginning_date)
            currencies.append(filename)
            json_currencies[filename] = beginning_date
            json_currencies_volume[filename] = volume

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
