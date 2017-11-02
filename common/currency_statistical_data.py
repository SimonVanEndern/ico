from typing import Dict, Tuple

import numpy
import pandas
from scipy import stats, math
from scipy.stats._stats_mstats_common import LinregressResult


class CurrencyStatisticalData:
    def __init__(self, currency: 'Currency'):
        self.currency: 'Currency' = currency

        self.first_date = self.calculate_fist_date()
        self.total_data_points = self.calculate_total_data_points()

        self.total_volume: float = self.calculate_total_volume()
        self.average_volume: float = self.calculate_average_volume()
        self.volume_linear_regression: LinregressResult = self.calculate_volume_linreg()

        self.highest_market_capitalization: float = self.calculate_highest_market_capitalization()
        self.average_market_capitalization: float = self.calculate_average_market_capitalization()
        self.market_capitalization_linear_regression: LinregressResult = self.calculate_market_capitalization_linreg()

        self.highest_price = self.calculate_highest_price()
        self.lowest_price = self.calculate_lowest_price()
        self.first_price = self.calculate_first_price()
        self.last_price = self.calculate_last_price()

        self.average_price: float = self.calculate_average_price()
        self.price_linear_regression: LinregressResult = self.calculate_usd_linreg()

        self.highest_price_difference: float
        self.price_change_from_beginning: float = self.calculate_price_change_from_beginning()

        self.volatilities: pandas.DataFrame = self.calculate_rolling_volatility()
        # TODO: Make it work
        # self.volatility_linear_regression: LinregressResult = self.calculate_volatility_linreg()

        self.google_trends_correlations: dict

        self.percentage_of_total_market_capitalization: pandas.DataFrame

        self.volume_return_correlations: dict = self.calculate_volume_return_correlations()
        self.price_market_capitalization_correlation: float = self.calculate_price_market_capitalization_correlation()

        # TODO: Maximum loss in terms of highest price / lowest price after this one
        # TODO: Same for highest gain

    def calculate_total_volume(self) -> float:
        return self.currency.data["volume"].sum()

    def calculate_average_volume(self) -> float:
        return float(numpy.mean(self.currency.data["volume"]))

    def calculate_average_market_capitalization(self) -> float:
        return float(numpy.mean(self.currency.data["market_cap"]))

    def calculate_average_price(self) -> float:
        return float(numpy.mean(self.currency.data["usd"]))

    def calculate_highest_market_capitalization(self) -> float:
        return max(self.currency.data["market_cap"])

    def calculate_highest_price(self) -> float:
        return max(self.currency.data["usd"])

    def calculate_lowest_price(self) -> float:
        return min(self.currency.data["usd"])

    def calculate_first_price(self) -> float:
        return list(self.currency.data["usd"])[0]

    def calculate_volume_return_correlations(self):
        shifts = [0, 1, 2, 3]
        volume = list(self.currency.relative_data["volume"])
        usd_return = list(self.currency.relative_data["usd"])

        while numpy.isnan(volume[0]) or numpy.isinf(volume[0]):
            volume.pop(0)
            usd_return.pop(0)

        output = dict()

        for shift in shifts:
            correlation_1 = stats.pearsonr(volume[shift:], usd_return[: len(usd_return) - shift])
            correlation_2 = stats.pearsonr(usd_return[shift:], volume[: len(volume) - shift])

            output[str(shift)] = correlation_1
            output[str(-shift)] = correlation_2

        return output

    def calculate_price_market_capitalization_correlation(self) -> float:
        return self.currency.relative_data.corr(method="pearson")["usd"]["market_cap"]

    def calculate_rolling_volatility(self, windows=None) -> Dict[str, pandas.DataFrame]:
        if windows is None:
            windows = [30, 90, 180]

        output: dict = dict()
        for window in windows:
            output[str(window)] = pandas.rolling_std(self.currency.relative_data, window)

        return output

    def calculate_volume_linreg(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamp"])
        volume = list(filled_data["volume"])

        return stats.linregress(timestamps, volume)

    def calculate_market_capitalization_linreg(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamp"])
        market_capitalization = list(filled_data["market_cap"])

        return stats.linregress(timestamps, market_capitalization)

    def calculate_usd_linreg(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamp"])
        usd = list(filled_data["usd"])

        return stats.linregress(timestamps, usd)

    def calculate_volatility_linreg(self) -> Dict[str, LinregressResult]:
        output = dict()
        for key in self.volatilities:
            timestamps = list(self.volatilities[key].index.values)
            volatility = list(self.volatilities[key]["usd"])

            while numpy.isnan(volatility[0]):
                volatility.pop(0)
                timestamps.pop(0)

            output[key] = stats.linregress(timestamps, volatility)

        return output

    def calculate_fist_date(self) -> int:
        return self.currency.data["timestamp"].iloc[0]

    def calculate_last_price(self) -> float:
        return self.currency.data["usd"].iloc[len(self.currency.data) - 1]

    def calculate_total_data_points(self) -> int:
        return len(self.currency.data)

    def calculate_price_change_from_beginning(self) -> float:
        if self.first_date != 0:
            return self.last_price / self.first_price - 1
        else:
            return math.inf
