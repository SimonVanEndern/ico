import csv
import os

from global_data import GlobalData
from top.statistical_analysis_calculator import StatisticalAnalysisCalculator


class StatisticalAnalysisRunnerAndExporter:
    def __init__(self, name, data):
        self.frame_name = name
        self.save_path = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name)
        self.data = data
        self.sac = StatisticalAnalysisCalculator(self.data)
        self.figure_counter = 1

        self.data = list()

    def save_plot(self, func):
        fig, fig_name = func()

        fig.suptitle("Figure " + str(self.figure_counter))
        fig.canvas.set_window_title("Figure " + str(self.figure_counter))

        fig.savefig(os.path.join(self.save_path, "Figure" + str(self.figure_counter) + "-" + fig_name + ".png"))

        self.figure_counter += 1

    def save_plots(self, func):
        fig1, fig2, fig_name1, fig_name2 = func()

        fig1.canvas.set_window_title("Figure " + str(self.figure_counter))
        fig2.canvas.set_window_title("Figure " + str(self.figure_counter))

        fig1.savefig(os.path.join(self.save_path, "Figure" + str(self.figure_counter) + "-" + fig_name1 + ".png"))
        self.figure_counter += 1
        fig2.savefig(os.path.join(self.save_path, "Figure" + str(self.figure_counter) + "-" + fig_name2 + ".png"))
        self.figure_counter += 1

    def add_correlation_data(self, name, func):
        correlation = func()
        self.data.append(
            (self.frame_name, name, "coefficient: " + str(correlation[0]), "p-value: " + str(correlation[1])))

    def add_correlations_data(self, name1, name2, func):
        corr1, corr2 = func()
        self.data.append((self.frame_name, name1, "coefficient: " + str(corr1[0]), "p-value: " + str(corr1[1])))
        self.data.append((self.frame_name, name2, "coefficient: " + str(corr2[0]), "p-value: " + str(corr2[1])))

    def add_mean_and_count_data_multiple(self, name1, name2, func):
        des1, des2 = func()
        self.data.append((self.frame_name, name1, "mean: " + str(des1["mean"]), "count: " + str(des1["count"])))
        self.data.append((self.frame_name, name2, "mean: " + str(des2["mean"]), "count: " + str(des2["count"])))

    def run(self):
        if not os.path.isdir(self.save_path):
            os.mkdir(self.save_path)

        # Average volume plot
        self.save_plot(self.sac.get_average_volume_data)

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
        self.data.append((self.frame_name,
                          "Average of average market capitalization divided by average volume",
                          "mean: " + str(mean),
                          "median: " + str(median)))

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
                                              "Mean of correlation volume and market capitalization only significant ones",
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
        self.data.append((self.frame_name,
                          "Currencies with positive linear regression slope and interploation limit=1",
                          "positives: " + str(positives)))
        self.data.append((self.frame_name,
                          "Currencies with negative linear regression slope and interploation limit=1",
                          "negatives: " + str(negatives)))
        self.data.append((self.frame_name,
                          "Currencies with positive linear regression slope and unlimited interpolation",
                          "positives: " + str(positives2)))
        self.data.append((self.frame_name,
                          "Currencies with negative linear regression slope and unlimited interpolation",
                          "negatives: " + str(negatives2)))

        # Correlations of volume and price raw data
        self.save_plot(self.sac.get_absolute_volume_price_correlation_plot)

        # Stats:
        # Descriptive statistics of volume and price raw data correlations
        self.add_mean_and_count_data_multiple("Mean of correlation volume and price all (excluding nans)",
                                              "Mean of correlation volume and price only significant ones (excluding nan)",
                                              self.sac.get_absolute_volume_price_correlation_data)

        # Figure:
        # First price since listing on coinmarketcap
        self.save_plot(self.sac.get_first_price_plot)

        # Figure:
        # Price change since beginning
        self.save_plot(self.sac.get_price_change_beginning_plot)

        with open(os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY, self.frame_name, "data.csv"), "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in self.data:
                writer.writerow(list(row))
