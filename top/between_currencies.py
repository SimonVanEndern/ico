from typing import Dict, Tuple

import matplotlib.pyplot as plt
import numpy
import pandas

from common.currency_handler import CurrencyHandler


class BetweenCurrencies:
    def __init__(self, save_path, currencies, attribute, start_date, sleep=False):
        self.correlations: Dict[str, Dict[str, Tuple[float, float]]] = dict()
        self.as_list = list()
        if sleep:
            return
        self.currency_handler = CurrencyHandler.Instance()
        self.attribute = attribute
        self.start_date = start_date

        self.save_path = save_path

        self.all_currencies = currencies

        self.counter = 0
        self.max = len(self.all_currencies) ** 2 / 2

        self.run()

    def run(self):
        print("Started Between Currencies for " + self.attribute + " and " + self.start_date)
        for index, currency in enumerate(self.all_currencies):
            if index == len(self.all_currencies) - 1:
                break
            self.correlations[currency] = dict()
            for index2, currency2 in enumerate(self.all_currencies[index + 1:]):
                correlation = self.currency_handler.get_currency(currency,
                                                                 date_limit=self.start_date).get_relative_correlation(
                    self.attribute,
                    self.currency_handler.get_currency(
                        currency2))
                self.counter += 1

                if self.counter % 10000 == 0:
                    print("Status: {}/{}".format(self.counter, self.max))

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
        ax.set(xlabel=self.attribute + " correlation between crypto-currencies", ylabel="Frequency")
        as_list = list(filter(lambda x: numpy.isfinite(x[2]), self.as_list))
        series_all = pandas.Series(list(map(lambda x: x[2], as_list)))
        significant = list(filter(lambda x: numpy.isfinite(x[3]) and x[3] < 0.1, as_list))
        series_significant = pandas.Series(list(map(lambda x: x[2], significant)))
        if not multiple:
            series_all.hist(ax=ax,
                            label="All calculated correlations: " + str(len(as_list)) + " observations",
                            bins=numpy.linspace(-1, 1, num=20)).plot()
            series_significant.hist(ax=ax,
                                    label="Correlations significant at 10%: " + str(len(significant)) + " observations",
                                    bins=numpy.linspace(-1, 1, num=20)).plot()
        else:
            series_significant.hist(ax=ax, color="C1", alpha=.8,
                                    label=legend_name + " (only if significant at 10%: " + str(
                                        len(series_significant)) + " of " + str(len(self.as_list)) + ")",
                                    bins=numpy.linspace(-1, 1, num=20)).plot(
                figure=fig)
        plt.legend(prop={'size': 8})

        return fig, ax, self.attribute + "-correlations-between-crypto-currencies"

    def get_correlation_positive_section_data(self):
        correlations = list(filter(lambda x: numpy.isfinite(x[2]), self.as_list))
        significant_correlations = list(filter(lambda x: numpy.isfinite(x[3]) and x[3] < 0.1, correlations))
        significant_correlations = list(map(lambda x: x[2], significant_correlations))
        positives = list(filter(lambda x: x > 0, significant_correlations))
        series = pandas.Series(positives)

        return series.describe().to_dict()

    def get_correlation_negative_section_data(self):
        correlations = list(filter(lambda x: numpy.isfinite(x[2]), self.as_list))
        significant_correlations = list(filter(lambda x: numpy.isfinite(x[3]) and x[3] < 0.1, correlations))
        significant_correlations = list(map(lambda x: x[2], significant_correlations))
        negatives = list(filter(lambda x: x <= 0, significant_correlations))
        series = pandas.Series(negatives)

        return series.describe().to_dict()
