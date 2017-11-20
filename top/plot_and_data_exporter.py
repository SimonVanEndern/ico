import csv
import os

import matplotlib.pyplot as plt

from global_data import GlobalData
from top.between_currencies import BetweenCurrencies
from top.calculation_result import CalculationResult
from top.cluster_result_container import ClusterResultContainer
from top.statistical_analysis_calculator import StatisticalAnalysisCalculator


class StatisticalAnalysisRunnerAndExporter:
    def __init__(self, name, data, subfolder=None):
        self.original_data: dict = data
        self.frame_name: str = name
        self.save_path: str = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name)
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        if subfolder is not None:
            self.save_path = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name, subfolder)
        self.sac: StatisticalAnalysisCalculator = StatisticalAnalysisCalculator(data)
        self.figure_counter: int = 1

        self.data = list()
        self.data_to_export = ClusterResultContainer(self.frame_name, "no_cluster")

    def save_plot(self, func) -> None:
        fig, ax, fig_name = func()

        # fig.suptitle("Figure " + str(self.figure_counter) + fig_name)
        fig.canvas.set_window_title("Figure " + str(self.figure_counter))

        self.save_figure(fig, fig_name)

    def save_figure(self, fig, fig_name) -> None:
        fig.set_size_inches(6, 4)
        fig.savefig(os.path.join(self.save_path, "Figure" + str(self.figure_counter) + "-" + fig_name + ".png"))
        plt.close(fig)

        self.figure_counter += 1

    def save_plots(self, func) -> None:
        fig1, fig2, fig_name1, fig_name2 = func()

        # fig1.suptitle("Figure " + str(self.figure_counter) + fig_name1)
        # fig2.suptitle("Figure " + str(self.figure_counter) + fig_name2)
        fig1.canvas.set_window_title("Figure " + str(self.figure_counter))
        fig2.canvas.set_window_title("Figure " + str(self.figure_counter))

        self.save_figure(fig1, fig_name1)
        self.save_figure(fig2, fig_name2)

    def add_correlation_data(self, name, func) -> None:
        correlation = func()
        self.data.append(
            (self.frame_name, name, "coefficient: " + str(correlation[0]), "p-value: " + str(correlation[1])))

        result = CalculationResult(name, "coefficient", correlation[0], "p-value", correlation[1])
        self.data_to_export.add_result(result, name)

    def add_correlations_data(self, name1, name2, func) -> None:
        corr1, corr2 = func()
        self.data.append((self.frame_name, name1, "coefficient: " + str(corr1[0]), "p-value: " + str(corr1[1])))
        self.data.append((self.frame_name, name2, "coefficient: " + str(corr2[0]), "p-value: " + str(corr2[1])))

        result = CalculationResult(name1, "coefficient", corr1[0], "p-value", corr1[1])
        result2 = CalculationResult(name2, "coefficient", corr2[0], "p-value", corr2[1])
        self.data_to_export.add_result(result, name1)
        self.data_to_export.add_result(result2, name2)

    def add_mean_and_count_data_multiple(self, name1, name2, func) -> None:
        des1, des2 = func()
        self.data.append((self.frame_name, name1, "mean: " + str(des1["mean"]), "count: " + str(des1["count"])))
        self.data.append((self.frame_name, name2, "mean: " + str(des2["mean"]), "count: " + str(des2["count"])))

        result = CalculationResult(name1, "mean", des1["mean"], "count", des1["count"])
        result2 = CalculationResult(name2, "mean", des2["mean"], "count", des2["count"])
        self.data_to_export.add_result(result, name1)
        self.data_to_export.add_result(result2, name2)

    def run(self) -> None:
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)

        # Average volume plot
        self.save_plot(self.sac.get_average_volume_plot)

        # Average market capitalization plot
        self.save_plot(self.sac.get_average_market_capitalization_plot)

        # Stat8
        # Correlation between average volume and average market capitalization
        self.add_correlation_data("Correlation Average Volume and Average Market Capitalization",
                                  self.sac.get_correlation_between_average_volume_and_average_market_capitalization)

        # Average market capitalization divided by average volume
        self.save_plot(self.sac.get_average_market_capitalization_divided_by_average_volume_plot)

        # Stat9
        # Average average of this
        mean, median = self.sac.get_average_market_capitalization_divided_by_average_volume_data()
        name = "Average of average market capitalization divided by average volume"
        self.data.append((self.frame_name,
                          "Average of average market capitalization divided by average volume",
                          "mean: " + str(mean),
                          "median: " + str(median)))

        result = CalculationResult(name, "mean", mean, "median", median)
        self.data_to_export.add_result(result, name)

        # Correlation of price and volume change
        self.save_plot(self.sac.get_volume_return_correlation_plot)

        # Stat 10:
        # Descriptive statistics of price and volume change
        self.add_mean_and_count_data_multiple("Mean of correlation volume and return all",
                                              "Mean of correlation volume and return only significant ones",
                                              self.sac.get_volume_return_correlation_data)

        # Correlation of volume and market capitalization
        self.save_plot(self.sac.get_volume_market_capitalization_correlation_plot)

        # Stat
        # Descriptive statistics of volume and market capitalization correlation
        self.add_mean_and_count_data_multiple("Mean of correlation volume and market capitalization all",
                                              "Mean of correlation volume and market cap only significant ones",
                                              self.sac.get_volume_market_capitalization_correlation_data)

        # Figure 09:
        # Correlation of price and volume change predictor search
        # TODO
        # self.sac.get_volume_price_correlation_cause_search_plot()

        # Stat 10
        # Correlation between age and average market capitalization
        # Stat 11
        # Correlation between age and last market capitalization
        self.add_correlations_data("Age and average market capitalization correlation",
                                   "Age and last market capitalization correlation",
                                   self.sac.get_age_market_capitalization_correlations)

        # Stat 11
        # Correlation between age and average volume
        self.add_correlation_data("Age and average volume correlation",
                                  self.sac.get_age_average_volume_correlation)

        # Slope of linear regression on price
        self.save_plots(self.sac.get_linear_price_regressions_plot)

        # Stats
        positives, negatives, positives2, negatives2 = self.sac.get_linear_regression_data()

        name = "Currencies with positive linear regression slope and interploation limit=1"
        self.data.append((self.frame_name, name, "positives: " + str(positives)))
        result = CalculationResult(name, "positives", positives, "", "")
        self.data_to_export.add_result(result, name)

        name = "Currencies with negative linear regression slope and interploation limit=1"
        self.data.append((self.frame_name, name, "negatives: " + str(negatives)))
        result = CalculationResult(name, "negatives", negatives, "", "")
        self.data_to_export.add_result(result, name)

        name = "Currencies with positive linear regression slope and unlimited interpolation"
        self.data.append((self.frame_name, name, "positives: " + str(positives2)))
        result = CalculationResult(name, "positives", positives2, "", "")
        self.data_to_export.add_result(result, name)

        name = "Currencies with negative linear regression slope and unlimited interpolation"
        self.data.append((self.frame_name, name, "negatives: " + str(negatives2)))
        result = CalculationResult(name, "negatives", negatives2, "", "")
        self.data_to_export.add_result(result, name)

        # Correlations of volume and price raw data
        self.save_plot(self.sac.get_absolute_volume_price_correlation_plot)

        # Stats:
        # Descriptive statistics of volume and price raw data correlations
        self.add_mean_and_count_data_multiple("Mean of correlation volume and price all (excluding nans)",
                                              "Mean of correlation volume and price only significant ones (excl nan)",
                                              self.sac.get_absolute_volume_price_correlation_data)

        # Figure:
        # First price since listing on coinmarketcap
        self.save_plot(self.sac.get_first_price_plot)

        # Figure:
        # Price change since beginning
        self.save_plot(self.sac.get_price_change_beginning_plot)

        # Figure:
        # Price correlation with google trends
        self.save_plot(self.sac.get_google_trends_correlation_plot)
        self.save_plot(self.sac.get_google_trends_correlation_plot2)

        with open(os.path.join(self.save_path, "data.csv"), "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in self.data:
                writer.writerow(list(row))

        self.data_to_export.save(self.save_path)

        BetweenCurrencies(self.save_path, list(self.original_data.keys()), sleep=True)
