from datetime import datetime
from pprint import pprint
from typing import Tuple, Dict, List, Any

import matplotlib.pyplot as plt
import numpy
from matplotlib import ticker
from pandas import Series, DataFrame
from scipy.stats import stats

from common.currency_handler import CurrencyHandler


def get_correlation_series_descriptions(correlations):
    correlations_all = list(map(lambda x: x[0], correlations))
    correlations_significant = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))
    correlations_significant = list(filter(lambda x: x != 0, correlations_significant))

    series = Series(correlations_all)
    series2 = Series(correlations_significant)

    return series.describe(), series2.describe()


def get_correlation_figure_from_correlations_list(correlations: List[Tuple[float, float]], xlabel=None):
    correlations_all: List[float] = list(map(lambda x: x[0], correlations))
    correlations_significant: List[float] = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations))
    correlations_significant = list(filter(lambda x: x != 0, correlations_significant))

    fig, ax = plt.subplots()
    ax.set(ylabel="Frequency")
    if xlabel is not None:
        ax.set(xlabel=xlabel)
    series = Series(correlations_all, name="All correlations")
    series.hist(ax=ax, bins=20, label="All correlations", alpha=0.8).plot()

    series = Series(correlations_significant, name="Correlations significant at 0.1")
    series.hist(ax=ax, bins=20, label="Correlations significant at 0.1", alpha=0.5).plot()
    plt.legend()

    return fig, ax


class StatisticalAnalysisCalculator:
    def __init__(self, data):
        self.data = data

        self.currency_handler = CurrencyHandler.Instance()

    def _get_series_of_attribute(self, attribute: str) -> Series:
        output = list()

        for key in self.data:
            output.append(getattr(self.data[key], attribute))

        return Series(output)

    def _get_pearsonr(self, attribute_1: str, attribute_2: str):
        list_1 = list()
        list_2 = list()

        for key in self.data:
            list_1.append(getattr(self.data[key], attribute_1))
            list_2.append(getattr(self.data[key], attribute_2))

        return stats.pearsonr(list_1, list_2)

    def get_average_volume_plot(self, fig=None, ax=None, multiple=False) -> Tuple[Any, Any, str]:
        series = self._get_series_of_attribute("average_volume")

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        fig.suptitle("Historgram of average volume in USD")
        ax.set(xlabel="Average Volume in USD", ylabel="Frequency")

        ax.set(ylabel="Frequency")
        series = numpy.log10(series)
        series = series[numpy.isfinite(series)]
        if not multiple:
            series.hist(ax=ax, bins=30, figure=fig).plot()
        else:
            series.hist(ax=ax, bins=30, figure=fig, alpha=0.8).plot()
        # series.hist(ax=ax, bins=numpy.logspace(0, 30, num=30, base=2))
        # ax.set_xscale('log', basex=10)
        return fig, ax, "average-volume-plot"

    def get_average_market_capitalization_plot(self, fig=None, ax=None, multiple=False):
        series = self._get_series_of_attribute("average_market_capitalization")

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        fig.suptitle("Historgram of average market capitalization in USD")
        ax.set(xlabel="Average market capitalization in USD", ylabel="Frequency")
        series = numpy.log10(series)
        series = series[numpy.isfinite(series)]
        if not multiple:
            series.hist(ax=ax, bins=30).plot()
        else:
            series.hist(ax=ax, bins=30, alpha=.8)
        # series.hist(ax=ax, bins=numpy.logspace(0, 15, num=30, base=10))
        # ax.set_xscale('log', basex=10)
        return fig, ax, "average-market-capitalization-plot"

    def get_correlation_between_average_volume_and_average_market_capitalization(self) -> Tuple[float, float]:
        return self._get_pearsonr("average_volume", "average_market_capitalization")

    def get_average_market_capitalization_divided_by_average_volume_plot(self, fig=None, ax=None, multiple=False):
        volume = list()
        market_cap = list()

        for key in self.data:
            volume.append(self.data[key].average_volume)
            market_cap.append(self.data[key].average_market_capitalization)

        combined = numpy.array(market_cap) / numpy.array(volume)
        combined = combined[numpy.isfinite(combined)]

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        fig.suptitle("Histogram of average market cap / average volume")
        ax.set(xlabel="average market cap / average volume", ylabel="Frequency")
        series = Series(combined)
        if not multiple:
            series.hist(ax=ax, bins=numpy.logspace(0, 16, num=16, base=2)).plot(spacing=0.5)
        else:
            series.hist(ax=ax, bins=numpy.logspace(0, 16, num=16, base=2), alpha=.8).plot(spacing=0.5)
        ax.set_xscale('log', basex=10)
        return fig, ax, "average-market-capitalization-divided-by-average-volume"

    def get_average_market_capitalization_divided_by_average_volume_data(self):
        volume = list()
        market_cap = list()

        for key in self.data:
            volume.append(self.data[key].average_volume)
            market_cap.append(self.data[key].average_market_capitalization)

        combined = numpy.array(market_cap) / numpy.array(volume)

        average = combined.mean()
        return 1 / average, 1 / numpy.median(combined)

    def get_volume_return_correlation_plot(self, fig=None, ax=None, multiple=False):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_return_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        fig, ax = get_correlation_figure_from_correlations_list(correlations)

        return fig, ax, "volume-return-correlations-plot-significant-marked"

    def get_volume_return_correlation_data(self):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_return_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        return get_correlation_series_descriptions(correlations)

    def get_volume_market_capitalization_correlation_plot(self, fig=None, ax=None, multiple=False):
        correlations: List[[Tuple[float, float]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_market_capitalization_correlation)

        fig, ax = get_correlation_figure_from_correlations_list(correlations)

        return fig, ax, "volume-market-cap-correlations-plot-significant-ones-marked"

    def get_volume_market_capitalization_correlation_data(self):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_market_capitalization_correlation)

        return get_correlation_series_descriptions(correlations)

    def get_absolute_volume_price_correlation_plot(self, fig=None, ax=None, multiple=False):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_price_correlations)

        correlations = list(map(lambda x: x["0"], correlations))

        fig, ax = get_correlation_figure_from_correlations_list(correlations,
                                                                xlabel="Correlation between volume and price")
        fig.suptitle("Histogram of correlations between volume and price")

        return fig, ax, "raw-volume-price-correlations-significant-marked"

    def get_absolute_volume_price_correlation_data(self):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()

        for key in self.data:
            correlations.append(self.data[key].volume_price_correlations)

        correlations = list(map(lambda x: x["0"], correlations))
        return get_correlation_series_descriptions(correlations)

    def get_volume_price_correlation_cause_search_plot(self):
        correlations: List[Dict[str, [Tuple[float, float]]]] = list()
        names = list()

        for key in self.data:
            correlations.append(self.data[key].volume_return_correlations)
            names.append(self.data[key].currency.currency)

        correlations_0 = list(map(lambda x: x["0"], correlations))
        correlations_adjusted = list(map(lambda x: x[0] if x[1] < 0.1 else 0, correlations_0))
        names_adjusted = list()
        for index, element in enumerate(correlations_adjusted):
            if element != 0:
                names_adjusted.append(names[index])

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
        Series(currency_characteristics_1).hist(bins=20).plot()
        plt.show()

        # Figure 12
        Series(currency_characteristics_2).hist(bins=20).plot()
        plt.show()

    def get_age_market_capitalization_correlations(self) -> Tuple[Any, Any]:
        age = list(map(lambda x: x.age_in_days, self.data.values()))
        average_market_capitalization = list(map(lambda x: x.average_market_capitalization, self.data.values()))
        last_market_capitalization = list(map(lambda x: x.last_market_capitalization, self.data.values()))
        last_market_capitalization = list(map(lambda x: 0 if numpy.isnan(x) else x, last_market_capitalization))

        return stats.pearsonr(age, average_market_capitalization), stats.pearsonr(age, last_market_capitalization)

    def get_age_average_volume_correlation(self) -> Tuple[float, float]:
        age = list(map(lambda x: x.age_in_days, self.data.values()))
        average_volume = list(map(lambda x: x.average_volume, self.data.values()))

        return stats.pearsonr(age, average_volume)

    def get_linear_price_regressions_plot(self):
        linear_regressions = list()
        linear_regressions_completely_interpolated = list()

        for item in self.data.values():
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
        fig.suptitle("Histogram of log10 linear regression slope")
        ax.set(ylabel="Frequency")
        ax.set(xlabel="log 10 slope of linear regression slope")
        series: Series = Series(linear_regressions)
        series.hist(bins=2, ax=ax).plot()

        fig2, ax2 = plt.subplots()
        series = Series(linear_regressions_completely_interpolated)
        series.hist(bins=2, ax=ax2).plot()

        return fig, fig2, "linear-regression-slope-limited-interpolation", "linear-regression-slope-unlimited-interpolation"

    def get_linear_regression_data(self):
        linear_regressions = list()
        linear_regressions_completely_interpolated = list()

        for item in self.data.values():
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

    def get_price_change_beginning_plot(self, fig=None, ax=None, multiple=False):
        series = self._get_series_of_attribute("price_change_from_beginning")
        if fig is None and ax is None:
            fig, ax = plt.subplots()
        ax.set(ylabel="Frequency")
        try:
            if not multiple:
                series.hist(ax=ax, bins=numpy.logspace(-8, 5, num=30, base=10)).plot(spacing=0.5)
            else:
                series.hist(ax=ax, bins=numpy.logspace(-8, 5, num=30, base=10), alpha=.8).plot(spacing=0.5)
        except ValueError:
            print(series)
        ax.set_xscale('log')
        ax.set(xlabel="last price divided by first available price")

        return fig, ax, "price-change-beginning-plot"

    def get_first_price_plot(self, fig=None, ax=None, multiple=False):
        series = self._get_series_of_attribute("first_price")

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        ax.set(ylabel="Frequency")
        if not multiple:
            series.hist(ax=ax, bins=numpy.logspace(-10, 5, num=100, base=10)).plot(spacing=0.5)
        else:
            series.hist(ax=ax, bins=numpy.logspace(-10, 5, num=100, base=10), alpha=.8).plot(spacing=0.5)
        ax.set_xscale('log')

        return fig, ax, "first-price-in-usd"

    def get_google_trends_correlation_plot(self, switch=0, fig=None, ax=None, multiple=False) -> Tuple[Any, Any, str]:
        if switch != 1 and switch != 0:
            raise Exception()
        trends = list()

        for key in self.data:
            if self.data[key].price_correlation_change_with_google_trends_data is not None:
                trends.append(self.data[key].price_correlation_change_with_google_trends_data[switch])

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        ax.set(ylabel="Frequency")
        series = Series(list(map(lambda x: x[0], trends)))
        series.hist(ax=ax, bins=20).plot(alpha=0.5)

        trends = list(map(lambda x: x[0] if x[1] < 0.1 else 0, trends))
        series = Series(trends)
        if not multiple:
            series[series != 0].hist(ax=ax, bins=20).plot()
        else:
            series[series != 0].hist(ax=ax, bins=20, alpha=.8).plot()

        return fig, ax, "google-trends-price-usd-correlation-significant-ones-marked"

    def get_google_trends_correlation_plot2(self, switch=1, fig=None, ax=None, multiple=False) -> Tuple[Any, Any, str]:
        if switch != 1 and switch != 2:
            raise Exception()
        trends = list()

        for key in self.data:
            if self.data[key].price_correlation_change_with_google_trends_data is not None:
                trends.append(self.data[key].price_correlation_change_with_google_trends_data[switch])

        if fig is None and ax is None:
            fig, ax = plt.subplots()
        ax.set(ylabel="Frequency")
        series = Series(list(map(lambda x: x[0], trends)))
        if not multiple:
            series.hist(ax=ax, bins=20).plot()
        else:
            series.hist(ax=ax, bins=20, alpha=.8).plot()

        trends = list(map(lambda x: x[0] if x[1] < 0.1 else 0, trends))
        series = Series(trends)
        series[series != 0].hist(ax=ax, bins=20).plot()

        return fig, ax, "google-trends-price-usd-correlation-significant-ones-marked"

    def get_first_date_plot(self, fig=None, ax=None, multiple=False):
        if fig is None and ax is None:
            fig, ax = plt.subplots()

        dates = self._get_series_of_attribute("first_date")

        df = DataFrame(list(dates), index=dates, columns=["date"]).sort_index()

        df["date"] = df["date"].astype("datetime64[ms]")
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).count()
        print(df2)

        df2.plot(kind="bar", ax=ax, legend=False)

        # Make most of the ticklabels empty so the labels don't get too crowded
        ticklabels = [''] * len(df2.index)
        # Every 4th ticklable shows the month and day
        ticklabels[::6] = [datetime(item[0], item[1], 1).strftime('%b %d') for item in df2.index[::6]]
        # Every 12th ticklabel includes the year
        ticklabels[::12] = [datetime(item[0], item[1], 1).strftime('%b %d\n%Y') for item in df2.index[::12]]
        ax.xaxis.set_major_formatter(ticker.FixedFormatter(ticklabels))
        fig.autofmt_xdate()

        # ax.set_xticklabels(index, rotation=90, fontsize=10)
        ax.set(xlabel="Time in months", ylabel="Frequency")
        ax.tick_params(labelsize=6)
        fig.subplots_adjust(bottom=0.3)

        return fig, ax, "start-dates"


    #>>> c.a.plot(kind="bar", ax=ax, width=.4, position=1, color="red")
    # <matplotlib.axes._subplots.AxesSubplot object at 0x0000015F2F480940>
    # >>> c.b.plot(kind="bar", ax=ax, width=.4, position=0, color="blue")
    # <matplotlib.axes._subplots.AxesSubplot object at 0x0000015F2F480940>
    # >>> plt.show()
