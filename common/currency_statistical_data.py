import numpy
import pandas
from scipy import stats
from scipy.stats._stats_mstats_common import LinregressResult

from common.currency import Currency


class CurrencyStatisticalData:
    def __init__(self, currency: Currency):
        self.currency: Currency = currency

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
        self.volatility_linear_regression: LinregressResult = self.calculate_volatility_linreg()

        self.google_trends_correlations: dict

        self.percentage_of_total_market_capitalization: pandas.DataFrame

        self.volume_return_correlations: dict = self.calculate_volume_return_correlations()
        self.price_market_capitalization_correlation: float = self.calculate_price_market_capitalization_correlation()

        # TODO: Maximum loss in terms of highest price / lowest price after this one
        # TODO: Same for highest gain

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

    def calculate_volume_linreg(self):
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamps"])
        volume = list(filled_data["volume"])

        return stats.linregress(timestamps, volume)

    def calculate_market_capitalization_linreg(self):
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamps"])
        market_capitalization = list(filled_data["market_cap"])

        return stats.linregress(timestamps, market_capitalization)

    def calculate_usd_linreg(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamps"])
        usd = list(filled_data["usd"])

        return stats.linregress(timestamps, usd)

    def calculate_volatility_linreg(self) -> dict(LinregressResult):
        output = dict()
        for key in self.volatilities:
            timestamps = list(self.volatilities[key]["timestamps"])
            volatility = list(self.volatilities[key]["volatility"])

            while numpy.isnan(volatility[0])
                volatility.pop(0)
                timestamps.pop(0)

            output[key] = stats.linregress(timestamps, volatility)

        return output

    def calculate_fist_date(self):
        return self.currency.data["timestamps"].iloc[0]

    def calculate_last_price(self):
        return self.currency.data["timestamps"].iloc[len(self.currency.data) - 1]

    def calculate_total_data_points(self):
        return len(self.currency.data)

    def calculate_price_change_from_beginning(self):
        if self.first_date != 0:
            return self.last_price / self.first_price - 1
        else:
            return numpy.inf
