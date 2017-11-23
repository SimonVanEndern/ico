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

        self.save_path = save_path

        self.all_currencies = currencies

        self.counter = 0
        self.max = len(self.all_currencies) ** 2 / 2

        self.correlations: Dict[str, Dict[str, Tuple[float, float]]] = dict()

        self.as_list = list()

        self.run()

    def run(self):
        for index, currency in enumerate(self.all_currencies):
            if index == len(self.all_currencies) - 1:
                break
            self.correlations[currency] = dict()
            for index2, currency2 in enumerate(self.all_currencies[index + 1:]):
                correlation = self.currency_handler.get_currency(currency).get_absolute_price_correlation(
                    self.currency_handler.get_currency(currency2))
                self.counter += 1

                print("Status: {}/{}".format(self.counter, self.max))
                print("Correlation of {} and {}: {}".format(currency, currency2, correlation))

                self.correlations[currency][currency2] = correlation

        for key in self.correlations:
            for key2 in self.correlations[key]:
                self.as_list.append((key, key2, self.correlations[key][key2][0], self.correlations[key][key2][1]))

        # with open(os.path.join(self.save_path, "all-correlations.csv"), "w") as file:
        #     writer = csv.writer(file, delimiter=",", lineterminator="\n")
        #     writer.writerow(["Currency1", "Currency2", "correlation", "p-value"])
        #     for row in self.as_list:
        #         writer.writerow(list(row))

    def get_correlation_plot(self, fig=None, ax=None, multiple=False, legend_name=""):
        if fig is None and ax is None:
            fig, ax = plt.subplots()
        ax.set(xlabel="Correlation", ylabel="Frequency")
        as_list = list(filter(lambda x: x[3] < 0.1, self.as_list))
        series2 = pandas.Series(list(map(lambda x: x[2], as_list)))
        if not multiple:
            series2.hist(ax=ax, color="C0", label=legend_name + " (only if significant at 10%: " + str(
                len(series2)) + " of " + str(len(self.as_list)) + ")").plot(figure=fig)
        else:
            series2.hist(ax=ax, color="C1", alpha=.8, label=legend_name + " (only if significant at 10%: " + str(
                len(series2)) + " of " + str(len(self.as_list)) + ")").plot(figure=fig)
            plt.legend(prop={'size': 6})

        return fig, ax, "correlations"

    def get_correlation_positive_section_data(self):
        all_correlations = list(map(lambda x: x[2], self.as_list))
        positives = list(filter(lambda x: x > 0, all_correlations))
        series = pandas.Series(positives)

        return series.describe().to_dict()

    def get_correlation_negative_section_data(self):
        all_correlations = list(map(lambda x: x[2], self.as_list))
        positives = list(filter(lambda x: x <= 0, all_correlations))
        series = pandas.Series(positives)

        return series.describe().to_dict()
