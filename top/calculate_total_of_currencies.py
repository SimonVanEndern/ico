import csv
from datetime import datetime

import matplotlib.pyplot as plt
import pandas

from common.currency_handler import CurrencyHandler


class TotalCalculator:
    currency_handler = CurrencyHandler.Instance()
    total_data: pandas.DataFrame = None

    def __init__(self):
        for currency in self.currency_handler.get_all_currency_names():
            handle_on_currency = self.currency_handler.get_currency(currency)

            if self.total_data is None:
                self.total_data = handle_on_currency.data
            else:
                self.total_data = self.total_data.add(handle_on_currency.data, axis='index', fill_value=0)

        timestamp = self.total_data.index.values
        usd = self.total_data["usd"]
        btc = self.total_data["btc"]
        volume = self.total_data["volume"]
        market_cap = self.total_data["market_cap"]

        for_export = zip(timestamp, usd, btc, volume, market_cap)

        with open("total.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["Timestamp", "USD", "BTC", "Volume", "Market_cap"])

            for row in for_export:
                writer.writerow(list(row))

        print(list(timestamp))
        print(list(market_cap))
        dates = list(map(lambda x: datetime.fromtimestamp(x / 1e3), list(timestamp)))

        fig, ax = plt.subplots()
        df = pandas.DataFrame(list(market_cap), index=dates)
        df.plot(ax=ax)
        plt.show()

        fig2, ax2 = plt.subplots()
        df2 = pandas.DataFrame(list(volume), index=dates)
        df2.plot(ax=ax2)
        plt.show()

        self.calculate_market_capitalization_collapses(market_cap)

    def calculate_market_capitalization_collapses(self, market_cap: pandas.DataFrame):
        indices = market_cap.index.values

        values = list(market_cap)

        output = list()

        for index, value in enumerate(values):
            if index < 980:
                continue
            lowest_value_afterwards = value
            index_of_lowest_value = index

            for index2, other_value in enumerate(values[index:]):
                if other_value < lowest_value_afterwards:
                    lowest_value_afterwards = other_value
                    index_of_lowest_value = index + index2

            output.append((lowest_value_afterwards / value - 1, index, index_of_lowest_value))

        output = sorted(output, key=lambda x: x[0])
        print(output)


TotalCalculator()
