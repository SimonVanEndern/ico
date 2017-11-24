import csv
from typing import List

import matplotlib.pyplot as plt
import numpy
import pandas

from common.currency import Currency
from common.currency_handler import CurrencyHandler


class PriceIndices:
    currency_handler = CurrencyHandler.Instance()

    def __init__(self):
        self.results = dict()

        all_currency_names = self.currency_handler.get_all_currency_names()
        self.all_currencies: List[Currency] = list(map(lambda x: self.currency_handler.get_currency(x), all_currency_names))

        self.bitcoin: Currency = self.currency_handler.get_currency("bitcoin")

    def run(self):
        fig, ax = plt.subplots()
        fig, ax = self.calculates_marekt_capitalization_weighted("market_cap", 1, 0, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("volume", 1, 0, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("market_cap", .2, 0, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("volume", .2, 0, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("market_cap", 1, 10000, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("volume", 1, 10000, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("market_cap", .2, 10000, fig, ax)
        fig, ax = self.calculates_marekt_capitalization_weighted("volume", .2, 10000, fig, ax)

        self.export()

        ax.set_yscale("log")
        plt.legend()
        plt.show()

    def calculates_marekt_capitalization_weighted(self, weight_name, max_weight, min_volume, fig, ax):
        weighted_return = dict()
        calculation_name = weight_name + "-weighted (max_weight=" + str(
            max_weight) + ", min_volume=" + str(min_volume) + ")"

        self.results["timestamp"] = self.bitcoin.data.index
        # total = Currency("total")

        for index in self.bitcoin.relative_data.index:
            for_weight_calculation = dict()
            for currency in self.all_currencies + [self.bitcoin]:
                if index in currency.data.index:
                    if currency.data.volume[index] >= min_volume:
                        for_weight_calculation[currency.currency] = currency.data[weight_name][index]
                    else:
                        for_weight_calculation[currency.currency] = 0
                else:
                    for_weight_calculation[currency.currency] = 0

            weights_to_use = self.calculate_weights(for_weight_calculation, max_weight)

            value = 0
            # print(index)
            for currency in self.all_currencies + [self.bitcoin]:
                if index in currency.relative_data.index and numpy.isfinite(currency.relative_data.usd[index]):
                    value += currency.relative_data.usd[index] * weights_to_use[currency.currency]

            weighted_return[index] = value

        # print(weighted_return)

        current = 100
        chart_index = dict()
        for key in sorted(weighted_return.keys()):
            current = current * (1 + weighted_return[key])
            chart_index[key] = current

        pandas.Series(list(chart_index.values())).plot(ax=ax,
                                                       label=calculation_name)

        self.results[calculation_name] = list(chart_index.values())

        return fig, ax

    def calculate_weights(self, slots: dict, max_weight):
        # print(slots)
        weights = dict()
        total = sum(list(slots.values()))

        # In case there are no weights at all
        if total == 0:
            return slots
        rest = 0
        exclude = list()
        for slot in slots:
            weights[slot] = slots[slot] / total
            if weights[slot] > max_weight:
                rest += (weights[slot] - max_weight) * total
                weights[slot] = max_weight
                exclude.append(slot)

        percentage_left = rest / total

        # In case all weights are nan or 0
        if rest == total:
            return weights
        while percentage_left > 0.0001:
            rest = 0
            current_total = 0
            for slot in slots:
                if slot not in exclude:
                    current_total += slots[slot]

            if current_total == 0:
                multiplier = 1 / (len(exclude) * max_weight)
                for weight in weights:
                    weights[weight] *= multiplier

                return weights

            for slot in slots:
                if slot not in exclude:
                    if weights[slot] + percentage_left * slots[slot] / current_total <= max_weight:
                        weights[slot] += percentage_left * slots[slot] / current_total
                    else:
                        exclude.append(slot)
                        rest += total * ((weights[slot] + percentage_left * slots[slot] / current_total) - max_weight)
                        weights[slot] = max_weight

            percentage_left = rest / total

        if not sum(weights.values()) <= 1.0001:
            print(weights)
            print(slots)
        assert (sum(weights.values()) <= 1.0001)
        return weights

    def export(self):
        with open("indices.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(sorted(self.results.keys()))

            for index in list(range(len(self.results["timestamp"]))):
                print(index)
                line = list()
                for key in sorted(self.results.keys()):
                    line.append(self.results[key][index])
                writer.writerow(line)


PriceIndices().run()
