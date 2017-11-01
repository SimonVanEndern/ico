from typing import Tuple

import numpy
import pandas
from scipy import stats

from common.currency import Currency


class CurrencyStatisticalData:
    def __init__(self, currency: Currency):
        self.currency: Currency = currency

        self.total_volume: float = self.calculate_total_volume()
        self.average_volume: float = self.calculate_average_volume()
        self.volume_linear_regression: Tuple(float, float)

        self.highest_market_capitalization: float = self.calculate_highest_market_capitalization()
        self.average_market_capitalization: float = self.calculate_average_market_capitalization()
        self.market_capitalization_linear_regression: Tuple(float, float)

        self.highest_price = self.calculate_highest_price()
        self.lowest_price = self.calculate_lowest_price()
        self.first_price = self.calculate_first_price()

        self.average_price: float = self.calculate_average_price()
        self.price_linear_regression: Tuple(float, float)

        self.highest_price_difference: float
        self.price_change_from_beginning: float

        self.volatility: pandas.DataFrame
        self.volatility_linear_regression: Tuple(float, float)

        self.google_trends_correlations: dict

        self.percentage_of_total_market_capitalization: pandas.DataFrame

        self.volume_return_correlations: dict = self.calculate_volume_return_correlations()
        self.price_market_capitalization_correlation: float = self.calculate_price_market_capitalization_correlation()

    def calculate_total_volume(self) -> float:
        return sum(self.currency.volume.data)

    def calculate_average_volume(self) -> float:
        return float(numpy.mean(self.currency.volume.data))

    def calculate_average_market_capitalization(self) -> float:
        return float(numpy.mean(self.currency.market_cap.data))

    def calculate_average_price(self) -> float:
        return float(numpy.mean(self.currency.usd.data))

    def calculate_highest_market_capitalization(self):
        return max(self.currency.market_cap.data)

    def calculate_highest_price(self):
        return max(self.currency.usd.data)

    def calculate_lowest_price(self):
        return min(self.currency.usd.data)

    def calculate_first_price(self):
        return self.currency.usd.data[0]

    def calculate_volume_return_correlations(self):
        # volume_return_correlation = self.currency.relative_data.corr(method="pearsonr")["volume"]["usd"]
        #
        shifts = [0, 1, 2, 3]
        volume = list(self.currency.relative_data["volume"])
        usd_return = list(self.currency.relative_data["usd"])

        output = dict()

        for shift in shifts:
            correlation_1 = stats.pearsonr(volume[shift:], usd_return[: len(usd_return) - 1 - shift])
            correlation_2 = stats.pearsonr(usd_return[shift:], volume[: len(volume) - 1 - shift])

            output[str(shift)] = correlation_1
            output[str(-shift)] = correlation_2

        return output

    def calculate_price_market_capitalization_correlation(self):
        return self.currency.relative_data.corr(method="pearsonr")["usd"]["market_cap"]

    def calculate_rolling_volatility(self, windows=None) -> dict:
        if windows is None:
            windows = [30, 90, 180]

        output: dict = dict()
        for window in windows:
            output[str(window)] = pandas.rolling_std(self.currency.relative_data["usd"], window)

        return output
