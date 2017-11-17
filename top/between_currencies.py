import csv
import os
from typing import Dict, Tuple

import matplotlib.pyplot as plt
import pandas

from common.currency_handler import CurrencyHandler


class BetweenCurrencies:
    def __init__(self, save_path, currencies, sleep=False):
        if sleep:
            return
        self.currency_handler = CurrencyHandler.Instance()

        all_currencies = currencies

        counter = 0
        max = len(all_currencies) ** 2 / 2

        correlations: Dict[str, Dict[str, Tuple[float, float]]] = dict()

        for index, currency in enumerate(all_currencies):
            if index == len(all_currencies) - 1:
                break
            correlations[currency] = dict()
            for index2, currency2 in enumerate(all_currencies[index + 1:]):
                correlation = self.currency_handler.get_currency(currency).get_absolute_price_correlation(
                    self.currency_handler.get_currency(currency2))
                counter += 1

                print("Status: {}/{}".format(counter, max))
                print("Correlation of {} and {}: {}".format(currency, currency2, correlation))

                correlations[currency][currency2] = correlation

        as_list = list()
        for key in correlations:
            for key2 in correlations[key]:
                as_list.append((key, key2, correlations[key][key2][0], correlations[key][key2][1]))

        with open(os.path.join(save_path, "all-correlations.csv"), "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["Currency1", "Currency2", "correlation", "p-value"])
            for row in as_list:
                writer.writerow(list(row))

        series = pandas.Series(list(map(lambda x: x[2], as_list)))
        series.hist().plot()

        plt.show()
