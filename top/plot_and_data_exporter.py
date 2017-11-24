import os
from typing import Callable

import matplotlib.pyplot as plt

from global_data import GlobalData
from top.between_currencies import BetweenCurrencies
from top.calculation_result import CalculationResult
from top.cluster_result_container import ClusterResultContainer
from top.statistical_analysis_calculator import StatisticalAnalysisCalculator


class StatisticalAnalysisRunnerAndExporter:
    def __init__(self, name, data, start_date: str, subfolder=None):
        self.original_data: dict = data
        self.frame_name: str = name
        self.save_path: str = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name)
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        if subfolder is not None:
            self.save_path = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name, subfolder)
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)
        self.sac: StatisticalAnalysisCalculator = StatisticalAnalysisCalculator(data)
        self.between_curr_usd: BetweenCurrencies = BetweenCurrencies(self.save_path, list(self.original_data.keys()),
                                                                     "usd", start_date, sleep=False)
        self.between_curr_volume: BetweenCurrencies = BetweenCurrencies(self.save_path, list(self.original_data.keys()),
                                                                        "volume", start_date, sleep=False)
        self.figure_counter: int = 1

        self.data = list()
        self.data_to_export: ClusterResultContainer = ClusterResultContainer(self.frame_name, "no_cluster")

    def save_plot(self, func: Callable) -> None:
        fig, ax, fig_name = func()
        fig.set_size_inches(7, 3.5)

        self.save_figure(fig, fig_name)

    def save_figure(self, fig, fig_name) -> None:
        fig.subplots_adjust(bottom=0.2, top=0.9)
        fig.savefig(os.path.join(self.save_path, "Figure" + str(self.figure_counter) + "-" + fig_name + ".png"))
        plt.close(fig)

        self.figure_counter += 1

    def save_plots(self, func: Callable) -> None:
        fig1, fig2, fig_name1, fig_name2 = func()
        fig1.set_size_inches(7, 3.5)
        fig2.set_size_inches(7, 3.5)

        fig1.canvas.set_window_title("Figure " + str(self.figure_counter))
        fig2.canvas.set_window_title("Figure " + str(self.figure_counter))

        self.save_figure(fig1, fig_name1)
        self.save_figure(fig2, fig_name2)

    def add_descriptive_data(self, result_name, func: Callable) -> None:
        result = CalculationResult(result_name, name_value_dict=func())
        self.data_to_export.add_result(result, result_name)

    def run(self) -> None:

        plot_functions = [self.sac.get_first_date_plot,
                          self.sac.get_average_volume_plot,
                          self.sac.get_average_market_capitalization_plot,
                          self.sac.get_average_volume_divided_by_average_market_capitalization_plot,
                          self.sac.get_log_volume_return_correlation_plot,
                          self.sac.get_volume_market_capitalization_correlation_plot,
                          self.sac.get_absolute_volume_price_correlation_plot,
                          self.sac.get_first_price_plot,
                          self.sac.get_price_change_beginning_plot,
                          self.sac.get_google_trends_correlation_plot,
                          self.sac.get_google_trends_correlation_plot2,
                          self.sac.get_volatility_plot]

        for plot_function in plot_functions:
            self.save_plot(plot_function)

        self.add_descriptive_data("Average volume data",
                                  self.sac.get_average_volume_data)
        self.add_descriptive_data("Average market capitalization data",
                                  self.sac.get_average_market_capitalization_data)
        self.add_descriptive_data("Correlation Average Volume and Average Market Capitalization",
                                  self.sac.get_correlation_between_average_volume_and_average_market_capitalization)
        self.add_descriptive_data("Histogram average volume / average market cap data",
                                  self.sac.get_average_volume_divided_by_average_market_capitalization_data)
        self.add_descriptive_data("correlation volume and return descriptives",
                                  self.sac.get_volume_return_correlation_data)
        self.add_descriptive_data("correlation volume and market capitalization descriptives",
                                  self.sac.get_volume_market_capitalization_correlation_positive_section_data)
        self.add_descriptive_data("correlation volume and market capitalization descriptives",
                                  self.sac.get_volume_market_capitalization_correlation_negative_section_data)

        self.add_descriptive_data("Google Trends correlation shift before, positive section",
                                  self.sac.get_google_trends_correlation_positive_section_data)
        self.add_descriptive_data("Google Trends correlation shift before, negative section",
                                  self.sac.get_google_trends_correlation_negative_section_data)
        self.add_descriptive_data("Google Trends correlation shift after, positive section",
                                  self.sac.get_google_trends_correlation_positive_section_data2)
        self.add_descriptive_data("Google Trends correlation shift after, negative section",
                                  self.sac.get_google_trends_correlation_negative_section_data2)

        # Figure 09:
        # Correlation of price and volume change predictor search
        # TODO
        # self.sac.get_volume_price_correlation_cause_search_plot()

        self.add_descriptive_data("Age and average market capitalization correlation",
                                  self.sac.get_age_average_market_capitalization_correlations)
        self.add_descriptive_data("Age and last market capitalization correlation",
                                  self.sac.get_age_last_market_capitalization_correlations)
        self.add_descriptive_data("Age and average volume correlation",
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

        self.add_descriptive_data("correlation volume and price data",
                                  self.sac.get_absolute_volume_price_correlation_data)

        self.add_descriptive_data("First price data", self.sac.get_first_price_data)
        self.add_descriptive_data("Price change beginning data", self.sac.get_price_change_beginning_data)
        self.add_descriptive_data("Volatility 90 window data", self.sac.get_volatility_data)

        self.save_plot(self.between_curr_usd.get_correlation_plot)
        self.save_plot(self.between_curr_volume.get_correlation_plot)
        # self.save_plot(self.between_curr_market_cap.get_correlation_plot)
        self.add_descriptive_data("Price correlations positive section",
                                  self.between_curr_usd.get_correlation_positive_section_data)
        self.add_descriptive_data("Price correlations negative section",
                                  self.between_curr_usd.get_correlation_negative_section_data)
        self.add_descriptive_data("Volume correlations positive section",
                                  self.between_curr_volume.get_correlation_positive_section_data)
        self.add_descriptive_data("Volume correlations negative section",
                                  self.between_curr_volume.get_correlation_negative_section_data)

        self.data_to_export.save(self.save_path)
