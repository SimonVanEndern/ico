from datetime import datetime
from pprint import pprint
from typing import List, Dict, Tuple, Any

import matplotlib.pyplot as plt
import numpy
import pandas
from scipy import stats

from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from top.within_currencies import WithinCurrencies


class LayerOnTopOfWithinCurrencies:
    def __init__(self):
        # Using data for whole period
        self.start_total: datetime = None

        # Using data from begin 2017 on
        self.start_2017: datetime = datetime.strptime("01.01.2017", "%d.%m.%Y")

        # Using data of last 6 month
        self.month_6: datetime = datetime.strptime("01.05.2017", "%d.%m.%Y")

        # Using data of last 3 month
        self.month_3: datetime = datetime.strptime("01.08.2017", "%d.%m.%Y")

        self.start_dates: List(datetime) = [self.start_total, self.start_2017, self.month_6, self.month_3]

        self.data: Dict[str, Dict[str, CurrencyStatisticalData]] = dict()

        for start_date in self.start_dates:
            if start_date is not None:
                break
            self.data[str(start_date)] = WithinCurrencies(start_date).get_and_export_data()

            # Clustering according to "coin" semantics
            self.data_semantic_cluster: Dict = dict()
            self.data_semantic_cluster["contains_keyword"], self.data_semantic_cluster[
                "no_keyword"] = self.filter_for_keyword()
            # Clustering according to available funding data
            # Clustering according to volume

        self.currency_handler = CurrencyHandler(static=True)

    def filter_for_keyword(self) -> Tuple[Dict, Dict]:
        contains_keyword = dict()
        no_keyword = dict()
        for start_date in self.data:
            data = self.data[start_date]
            for currency_statistical in data:
                if data[currency_statistical].currency.contains_keyword("any"):
                    contains_keyword[currency_statistical] = data[currency_statistical]
                else:
                    no_keyword[currency_statistical] = data[currency_statistical]

        return contains_keyword, no_keyword

    def get_keyword_data(self):
        standard_set = self.data["None"]
        index = list()
        figure_1 = list()
        for key in standard_set:
            currency = standard_set[key].currency
            item = (standard_set[key].first_date,
                    currency.contains_keyword("coin"),
                    currency.contains_keyword("token"),
                    currency.contains_keyword("bit"),
                    currency.contains_keyword("any"),
                    True)
            figure_1.append(item)
            index.append(standard_set[key].first_date)

        df = pandas.DataFrame(figure_1, index=index,
                              columns=["date", "coin", "token", "bit", "any", "all"]).sort_index()

        df["date"] = df["date"].astype("datetime64[ms]")
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).sum()
        df2["coin"] = df2["coin"] / df2["all"]
        df2["token"] = df2["token"] / df2["all"]
        df2["bit"] = df2["bit"] / df2["all"]
        df2["any"] = df2["any"] / df2["all"]
        del df2["all"]
        df2.plot(kind="bar")
        plt.show()

        return figure_1

    def get_start_time_analysis(self):
        standard_set = self.data["None"]
        index = list()
        output = list()

        for key in standard_set:
            index.append(standard_set[key].first_date)
            output.append(True)

        df = pandas.DataFrame(index, index=index, columns=["date"]).sort_index()

        df["date"] = df["date"].astype("datetime64[ms]")
        print(df)
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).count()
        print(df2)

        df2.plot(kind="bar")
        plt.show()

        return

    def get_average_volume_data(self):
        standard_set = self.data["None"]
        index = list()
        output = list()

        for key in standard_set:
            output.append(standard_set[key].average_volume)
            index.append(standard_set[key].first_date)

        series = pandas.Series(output)

        fig, ax = plt.subplots()
        series.hist(ax=ax, bins=numpy.logspace(0, 30, num=30, base=2))
        ax.set_xscale('log', basex=10)
        return fig, "average-volume-plot"

    def get_average_market_capitalization_plot(self):
        standard_set = self.data["None"]
        index = list()
        output = list()

        for key in standard_set:
            output.append(standard_set[key].average_market_capitalization)
            index.append(standard_set[key].first_date)

        series = pandas.Series(output)

        fig, ax = plt.subplots()
        series.hist(ax=ax, bins=numpy.logspace(0, 30, num=30, base=2))
        ax.set_xscale('log', basex=10)
        return fig, "average-market-capitalization-plot"

    def get_correlation_between_average_volume_and_average_market_capitalization(self):
        standard_set = self.data["None"]
        volume = list()
        market_cap = list()

        for key in standard_set:
            volume.append(standard_set[key].average_volume)
            market_cap.append(standard_set[key].average_market_capitalization)

        return stats.pearsonr(volume, market_cap)

    def get_average_market_capitalization_divided_by_average_volume_plot(self):
        standard_set = self.data["None"]
        volume = list()
        market_cap = list()

        for key in standard_set:
            volume.append(standard_set[key].average_volume)
            market_cap.append(standard_set[key].average_market_capitalization)

        combined = numpy.array(market_cap) / numpy.array(volume)

        fig, ax = plt.subplots()
        series = pandas.Series(combined)
        series.hist(ax=ax, bins=numpy.logspace(0, 16, num=16, base=2)).plot(spacing=0.5)
        ax.set_xscale('log')
        # plt.show()
        return fig, "average-market-capitalization-divided-by-average-volume"

    def get_average_market_capitalization_divided_by_average_volume_data(self):
        standard_set = self.data["None"]
        volume = list()
        market_cap = list()

        for key in standard_set:
            volume.append(standard_set[key].average_volume)
            market_cap.append(standard_set[key].average_market_capitalization)

        combined = numpy.array(market_cap) / numpy.array(volume)
        # print(list(combined))

        average = combined.mean()
        print("Average market capitalization / volume")
        return 1 / average, 1 / numpy.median(combined)
        # print(scipy.stats.describe(combined))

    def get_volume_return_correlation_plot(self):
        standard_set = self.data["None"]
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in standard_set:
            correlations.append(standard_set[key].volume_return_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        correlations_all = list(map(lambda x: x[0], correlations))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))

        fig, ax = plt.subplots()
        series = pandas.Series(correlations_all)
        series.hist(ax=ax, bins=20).plot()

        fig2, ax = plt.subplots()
        series = pandas.Series(correlations_adjusted)
        series.hist(ax=ax, bins=20).plot()

        return fig, fig2, "volume-return-correlations-plot", "volume-return-correlations-only-significatn-plot"

    def get_volume_return_correlation_data(self):
        standard_set = self.data["None"]
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in standard_set:
            correlations.append(standard_set[key].volume_return_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        correlations_all = list(map(lambda x: x[0], correlations))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))

        series = pandas.Series(correlations_all)

        series2 = pandas.Series(correlations_adjusted)

        return series.describe(), series2[series2 > 0].describe()

    def get_absolute_volume_price_correlation_plot(self):
        standard_set = self.data["None"]
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in standard_set:
            correlations.append(standard_set[key].volume_price_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        correlations_all = list(map(lambda x: x[0], correlations))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))

        fig, ax = plt.subplots()
        series = pandas.Series(correlations_all)
        series.hist(ax=ax, bins=20).plot()

        fig2, ax = plt.subplots()
        series = pandas.Series(correlations_adjusted)
        series.hist(ax=ax, bins=20).plot()

        return fig, fig2, "raw-volume-price-correlations", "raw-volume-price-correlations-only-significant"

    def get_absolute_volume_price_correlation_data(self):
        standard_set = self.data["None"]
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in standard_set:
            correlations.append(standard_set[key].volume_price_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        correlations_all = list(map(lambda x: x[0], correlations))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))

        series = pandas.Series(correlations_all)
        print("Description of statistics for all correlations")

        series2 = pandas.Series(correlations_adjusted)
        print("Description of statistics for only significant correlations, excluding 0")

        return series.describe(), series2[series2 > 0].describe()

    def get_volume_price_correlation_cause_search_plot(self):
        standard_set = self.data["None"]
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()
        names = list()

        for key in standard_set:
            correlations.append(standard_set[key].volume_return_correlations)
            names.append(standard_set[key].currency.currency)

        correlations_0 = list(map(lambda x: x["0"], correlations))
        correlations_all = list(map(lambda x: x[0], correlations_0))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations_0))
        names_adjusted = list()
        for index, element in enumerate(correlations_adjusted):
            if element != 0:
                names_adjusted.append(names[index])

        fig, ax = plt.subplots()
        series = pandas.Series(correlations_all)
        print("Description of statistics for all correlations")
        print(series.describe())
        print(series.median())
        series.hist(ax=ax, bins=20).plot()
        plt.title("Figure XX")
        fig.canvas.set_window_title("Figure XX")
        # fig.savefig('test.png')
        plt.show()

        series = pandas.Series(correlations_adjusted)
        print("Description of statistics for only significant correlations, excluding 0")
        print(series[series != 0].describe())
        print(series[series != 0].median())
        series[series != 0].hist(bins=20).plot()
        plt.show()

        shift_results = list()
        shift_results.append(("Shift", "mean", "median", "observations"))

        names_total = dict()

        for i in [-3, -2, -1, 0, 1, 2, 3]:
            results = list(map(lambda x: x[str(i)], correlations))
            results = list(map(lambda x: x[0] if x[1] < 0.1 else 0, results))
            results = list(filter(lambda x: x != 0, results))
            shift_results.append((i, numpy.mean(results), numpy.median(results), len(results)))

            for index, element in enumerate(results):
                if element != 0:
                    if names[index] in names_total:
                        names_total[names[index]] += 1
                    else:
                        names_total[names[index]] = 1

        pprint(shift_results)
        pprint(names_total)

        currency_characteristics_1 = list()
        currency_characteristics_2 = list()
        for currency in names_total:
            data = self.currency_handler.get_currency(currency)
            data.get_statistical_data()
            if names_total[currency] > 1:
                currency_characteristics_2.append(data.statistical_data.age_in_days)
            else:
                currency_characteristics_1.append(data.statistical_data.age_in_days)

        # Figure 11
        pandas.Series(currency_characteristics_1).hist(bins=20).plot()
        plt.show()

        # Figure 12
        pandas.Series(currency_characteristics_2).hist(bins=20).plot()
        plt.show()

    def get_age_market_capitalization_correlations(self) -> Tuple[Any, Any]:
        standard_set = self.data["None"]

        age = list(map(lambda x: x.age_in_days, standard_set.values()))
        average_market_capitalization = list(map(lambda x: x.average_market_capitalization, standard_set.values()))
        last_market_capitalization = list(map(lambda x: x.last_market_capitalization, standard_set.values()))
        last_market_capitalization = list(map(lambda x: 0 if numpy.isnan(x) else x, last_market_capitalization))

        return stats.pearsonr(age, average_market_capitalization), stats.pearsonr(age, last_market_capitalization)

    def get_age_average_volume_correlation(self) -> Tuple[float, float]:
        standard_set = self.data["None"]

        age = list(map(lambda x: x.age_in_days, standard_set.values()))
        average_volume = list(map(lambda x: x.average_volume, standard_set.values()))

        return stats.pearsonr(age, average_volume)

    def get_linear_price_regressions_plot(self):
        standard_set: Dict[str, CurrencyStatisticalData] = self.data["None"]

        linear_regressions = list()
        linear_regressions_completely_interpolated = list()

        for item in standard_set.values():
            # if item.price_linear_regression_standardized.pvalue > 0.1:
            #     print(item.currency.currency)
            if numpy.isnan(item.price_linear_regression_standardized.slope):
                if item.price_linear_regression_standardized.pvalue > 0.1:
                    print(item.currency.currency)
                linear_regressions_completely_interpolated.append(
                    item.price_linear_regression_standardized_completely_interpolated.slope)
            else:
                linear_regressions.append(item.price_linear_regression_standardized.slope)

        linear_regressions = list(map(lambda x: -numpy.log10(x) if x > 0 else numpy.log10(-x), linear_regressions))
        linear_regressions_completely_interpolated = list(
            map(lambda x: -numpy.log10(x) if x > 0 else numpy.log10(-x), linear_regressions_completely_interpolated))

        fig, ax = plt.subplots()
        series: pandas.Series = pandas.Series(linear_regressions)
        series.hist(bins=30).plot()

        fig2, ax = plt.subplots()
        series = pandas.Series(linear_regressions_completely_interpolated)
        series.hist(bins=30).plot()

        return fig, fig2, "linear-regression-slope-limited-interpolation", "linear-regression-slope-unlimited-interpolation"

    def get_linear_regression_data(self):
        standard_set = self.data["None"]

        linear_regressions = list()
        linear_regressions_completely_interpolated = list()

        for item in standard_set.values():
            if numpy.isnan(item.price_linear_regression_standardized.slope):
                linear_regressions_completely_interpolated.append(
                    item.price_linear_regression_standardized_completely_interpolated.slope)
            else:
                linear_regressions.append(item.price_linear_regression_standardized.slope)

        positives = len(list(filter(lambda x: x > 0, linear_regressions)))
        negatives = len(linear_regressions) - positives

        positives_interpolated = len(list(filter(lambda x: x > 0, linear_regressions_completely_interpolated)))
        negatives_interpolated = len(linear_regressions_completely_interpolated) - positives_interpolated

        return positives, negatives, positives_interpolated, negatives_interpolated
