from typing import Dict, Tuple, List

import numpy
import pandas
from scipy import stats, math
from scipy.stats._stats_mstats_common import LinregressResult

from global_data import GlobalData
from google_trends.import_data.google_trends_DTO import GoogleTrendsDTO


class CurrencyStatisticalData:
    def __init__(self, currency: 'Currency'):
        self.currency: 'Currency' = currency

        self.first_date: int = self.calculate_fist_date()
        self.total_data_points = self.calculate_total_data_points()
        self.age_in_days = (GlobalData.LAST_DATE_FOR_ANALYSIS - self.first_date) / (1000 * 3600 * 24)

        self.total_volume: float = self.calculate_total_volume()
        self.average_volume: float = self.calculate_average_volume()
        self.volume_linear_regression: LinregressResult = self.calculate_volume_linreg()

        self.highest_market_capitalization: float = self.calculate_highest_market_capitalization()
        self.last_market_capitalization: float = self.calculate_last_market_capitalization()
        self.average_market_capitalization: float = self.calculate_average_market_capitalization()
        self.market_capitalization_linear_regression: LinregressResult = self.calculate_market_capitalization_linreg()

        self.highest_price = self.calculate_highest_price()
        self.lowest_price = self.calculate_lowest_price()
        self.first_price = self.calculate_first_price()
        self.last_price = self.calculate_last_price()

        self.average_price: float = self.calculate_average_price()
        self.price_linear_regression: LinregressResult = self.calculate_usd_linreg()
        self.price_linear_regression_standardized: LinregressResult = self.calculate_usd_linreq_standardized()
        self.price_linear_regression_standardized_completely_interpolated: LinregressResult = self.calculate_usd_linreq_standardized_completely_interpolated()

        self.highest_price_difference: float
        self.price_change_from_beginning: float = self.calculate_price_change_from_beginning()

        self.volatilities: Dict[str, pandas.DataFrame] = self.calculate_rolling_volatility()
        self.average_volatility_90 = numpy.mean(self.volatilities["90"]["usd"])

        # TODO: Make it work
        # self.volatility_linear_regression: LinregressResult = self.calculate_volatility_linreg()

        self.google_trends_correlations: List[Tuple[int, float]] = self.load_google_trends_data()
        self.price_correlation_change_with_google_trends_data: Tuple[
            Tuple[float, float], Tuple[float, float]] = self.calculate_price_correlation_with_google_trends()

        self.percentage_of_total_market_capitalization: pandas.DataFrame

        self.volume_return_correlations: Dict[str, Tuple[float, float]] = self.calculate_volume_return_correlations()
        self.volume_market_capitalization_correlation: Tuple[
            float, float] = self.calculate_volume_market_capitalization_correlation()
        self.absolute_volume_price_correlations: Dict[
            str, Tuple[float, float]] = self.calculate_absolute_volume_price_correlations()
        self.price_market_capitalization_correlation: float = self.calculate_price_market_capitalization_correlation()

        self.correlation_other_currencies: Dict[str, Tuple[float, float]] = dict()

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
        prices = list(self.currency.data["usd"])
        if numpy.isnan(list(self.currency.data["usd"])[0]):
            print("NAN Price: " + self.currency.currency)
            print(list(self.currency.data["usd"]))
            i = 0
            while numpy.isnan(prices[i]):
                i += 1
                if i > len(prices) - 1:
                    raise RuntimeError("No data for this currency")
            price = prices[i]
        else:
            price = list(self.currency.data["usd"])[0]
        if list(self.currency.data["usd"])[0] > 100:
            print("Zu viel: " + self.currency.currency)

        return price

    def calculate_volume_return_correlations(self) -> Dict[str, Tuple[float, float]]:
        shifts = [0, 1, 2, 3]
        volume = list(self.currency.relative_data["volume"])
        usd_return = list(self.currency.relative_data["usd"])

        try:
            while numpy.isnan(volume[0]) or numpy.isinf(volume[0]):
                volume.pop(0)
                usd_return.pop(0)
        except IndexError:
            print(self.first_date)
            print(volume)
            print(self.currency.currency)
            return {"-3": (numpy.nan, numpy.nan),
                    "-2": (numpy.nan, numpy.nan),
                    "-1": (numpy.nan, numpy.nan),
                    "0": (numpy.nan, numpy.nan),
                    "1": (numpy.nan, numpy.nan),
                    "2": (numpy.nan, numpy.nan),
                    "3": (numpy.nan, numpy.nan)}

        output = dict()

        for shift in shifts:
            correlation_1 = stats.pearsonr(volume[shift:], usd_return[: len(usd_return) - shift])
            correlation_2 = stats.pearsonr(usd_return[shift:], volume[: len(volume) - shift])

            output[str(shift)] = correlation_1
            output[str(-shift)] = correlation_2

        return output

    def calculate_absolute_volume_price_correlations(self) -> Dict[str, Tuple[float, float]]:
        shifts = [0, 1, 2, 3]
        volume = list(self.currency.data["volume"])
        usd_return = list(self.currency.data["usd"])

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

    def calculate_volume_market_capitalization_correlation(self) -> Tuple[float, float]:
        volume = list(self.currency.data["volume"])
        market_cap = list(self.currency.data["market_cap"])

        combined = list()
        for index, element in enumerate(volume):
            if (not numpy.isnan(volume[index])) and (not numpy.isnan(market_cap[index])):
                combined.append((volume[index], market_cap[index]))

        if (len(volume) - len(combined)) / len(volume) > 0.1:
            print(self.currency.currency)
            print((len(volume) - len(combined)) / len(volume))
            print("WARNING: BAD DATA IN MAKRET CAP")

        volume, market_cap = zip(*combined)
        return stats.pearsonr(volume, market_cap)

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

    def calculate_usd_linreq_standardized(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate(limit=1)

        timestamps = list(filled_data["timestamp"])
        usd = list(filled_data["usd"])
        usd = numpy.array(usd)
        usd = usd / usd[len(usd) - 1]

        return stats.linregress(timestamps, usd)

    def calculate_usd_linreq_standardized_completely_interpolated(self) -> LinregressResult:
        filled_data = self.currency.data.interpolate()

        timestamps = list(filled_data["timestamp"])
        usd = list(filled_data["usd"])
        usd = numpy.array(usd)
        usd = usd / usd[len(usd) - 1]

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
        prices = list(self.currency.data["usd"])
        if numpy.isnan(self.currency.data["usd"].iloc[len(self.currency.data) - 1]):
            print("LAST PRICE: " + self.currency.currency)
            i = len(prices) - 1
            while numpy.isnan(prices[i]):
                i -= 1
            price = prices[i]
            if len(prices) - i > 10:
                print("WARNING: Bad data")
        else:
            price = self.currency.data["usd"].iloc[len(self.currency.data) - 1]

        return price

    def calculate_last_market_capitalization(self) -> float:
        return self.currency.data["market_cap"].iloc[len(self.currency.data) - 1]

    def calculate_total_data_points(self) -> int:
        return len(self.currency.data)

    def calculate_price_change_from_beginning(self) -> float:
        if self.first_price != 0:
            return self.last_price / self.first_price
        else:
            return math.inf

    def to_json_export(self) -> dict:
        export = self.__dict__.copy()
        export.pop("currency")

        for key in export["volume_return_correlations"]:
            export["volume_return_correlations_" + key + "-r-value"] = export["volume_return_correlations"][key][0]
            export["volume_return_correlations_" + key + "-p-value"] = export["volume_return_correlations"][key][1]

        return export

    def load_google_trends_data(self) -> List[Tuple[int, float]]:
        gtd = GoogleTrendsDTO(self.currency.currency)
        return gtd.load_aggregated_data()

    def calculate_price_correlation_with_google_trends(self) -> Tuple[Tuple[float, float], Tuple[float, float]]:
        if self.google_trends_correlations is None or len(self.google_trends_correlations) == 0:
            return None
        trends_adjusted = list(map(lambda x: ((x[0] + 12 * 3600) * 1000, x[1]), self.google_trends_correlations))
        trends_adjusted2 = list(map(lambda x: ((x[0] - 12 * 3600) * 1000, x[1]), self.google_trends_correlations))
        index, trends = zip(*trends_adjusted)
        index2, trends2 = zip(*trends_adjusted2)
        trends_df = pandas.DataFrame(list(trends), index=list(index))
        trends_df2 = pandas.DataFrame(list(trends2), index=list(index2))
        usd = self.currency.relative_data["usd"]

        combined: pandas.DataFrame = pandas.concat([usd, trends_df], axis=1)
        combined2: pandas.DataFrame = pandas.concat([usd, trends_df2], axis=1)
        combined.columns = ["a", "b"]
        combined2.columns = ["a", "b"]
        combined = combined.dropna()
        combined2 = combined2.dropna()

        return stats.pearsonr(list(combined["a"]), list(combined["b"])), stats.pearsonr(list(combined2["a"]),
                                                                                        list(combined2["b"]))
