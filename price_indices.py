from typing import List

import matplotlib.pyplot as plt
import numpy
import pandas

from common.currency import Currency
from common.currency_handler import CurrencyHandler


class PriceIndices:
    currency_handler = CurrencyHandler.Instance()

    def __init__(self):
        pass

    def calculates_marekt_capitalization_weighted(self, weight_name, max_weight, min_volume, fig, ax):
        weighted_return = dict()

        all_currency_names = self.currency_handler.get_all_currency_names()
        all_currencies: List[Currency] = list(map(lambda x: self.currency_handler.get_currency(x), all_currency_names))
        bitcoin: Currency = self.currency_handler.get_currency("bitcoin")
        # total = Currency("total")

        for index in bitcoin.relative_data.index:
            for_weight_calculation = dict()
            for currency in all_currencies + [bitcoin]:
                if index in currency.data.index:
                    if currency.data.volume[index] >= min_volume:
                        for_weight_calculation[currency.currency] = currency.data[weight_name][index]
                    else:
                        for_weight_calculation[currency.currency] = 0
                else:
                    for_weight_calculation[currency.currency] = 0

            weights_to_use = self.calculate_weights(for_weight_calculation, max_weight)

            value = 0
            print(index)
            for currency in all_currencies + [bitcoin]:
                if index in currency.relative_data.index and numpy.isfinite(currency.relative_data.usd[index]):
                    value += currency.relative_data.usd[index] * weights_to_use[currency.currency]

            weighted_return[index] = value

        print(weighted_return)

        current = 100
        chart_index = dict()
        for key in sorted(weighted_return.keys()):
            current = current * (1 + weighted_return[key])
            chart_index[key] = current

        print(chart_index)

        pandas.Series(list(chart_index.values())).plot(ax=ax,
                                                       label=weight_name + "-weighted (max_weight=" + str(
                                                           max_weight) + ", min_volume=" + str(min_volume) + ")")

        return fig, ax

    def calculate_weights(self, slots: dict, max_weight):
        weights = dict()
        total = sum(list(slots.values()))
        rest = 0
        exclude = list()
        for slot in slots:
            weights[slot] = slots[slot] / total
            if weights[slot] > max_weight:
                rest += (weights[slot] - max_weight) * total
                weights[slot] = max_weight
                exclude.append(slot)

        percentage_left = rest / total
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

        if sum(weights.values()) > 1:
            print(slots)
        assert (sum(weights.values()) <= 1)
        return weights


# fig, ax = plt.subplots()
# price_indices = PriceIndices()
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("market_cap", 1, 0, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("volume", 1, 0, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("market_cap", .2, 0, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("volume", .2, 0, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("market_cap", 1, 10000, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("volume", 1, 10000, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("market_cap", .2, 10000, fig, ax)
# fig, ax = price_indices.calculates_marekt_capitalization_weighted("volume", .2, 10000, fig, ax)
# ax.set_yscale("log")
# plt.legend()
# plt.show()
