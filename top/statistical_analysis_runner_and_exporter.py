import os

from global_data import GlobalData


class StatisticalAnalysisRunnerAndExporter:

    def __init__(self, name, data):
        self.name = name
        self.data = data

    def run(self):
        frame_name = self.name
        save_path = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA, frame_name)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        data = list()

        # Figure05:
        # Average volume plot
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_volume_data()
        fig.savefig(os.path.join(save_path, "Figure05-" + fig_name + ".png"))

        # Figure06:
        # Average market capitalization plot
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_market_capitalization_plot()
        fig.savefig(os.path.join(save_path, "Figure06-" + fig_name + ".png"))

        # Stat8
        # Correlation between average volume and average market capitalization
        correlation = self.layer_on_top_of_within_currencies.get_correlation_between_average_volume_and_average_market_capitalization()
        data.append((frame_name,
                     "Correlation Average Volume and Average Market Capitalization",
                     "coefficient: " + str(correlation[0]),
                     "p-value: " + str(correlation[1])))

        # Figure 07:
        # Average market capitalization divided by average volume
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_market_capitalization_divided_by_average_volume_plot()
        fig.savefig(os.path.join(save_path, "Figure07-" + fig_name + ".png"))

        # Stat9
        # Average average of this
        mean, median = self.layer_on_top_of_within_currencies.get_average_market_capitalization_divided_by_average_volume_data()
        data.append((frame_name,
                     "Average of average market capitalization divided by average volume",
                     "mean: " + str(mean),
                     "median: " + str(median)))

        # Figure 08:
        # Correlation of price and volume change
        fig, fig2, fig_name, fig_name2 = self.layer_on_top_of_within_currencies.get_volume_return_correlation_plot()
        fig.canvas.set_window_title("Figure XX")
        fig.savefig(os.path.join(save_path, "Figure08-" + fig_name + ".png"))
        fig2.savefig(os.path.join(save_path, "Figure09-" + fig_name2 + ".png"))

        # Stat 10:
        # Descriptive statistics of price and volume change
        des1, des2 = self.layer_on_top_of_within_currencies.get_volume_return_correlation_data()
        data.append((frame_name,
                     "Mean of correlation volume and return all",
                     "mean: " + str(des1["mean"]),
                     "count: " + str(des1["count"])))
        data.append((frame_name,
                     "Mean of correlation volume and return only significant ones",
                     "mean: " + str(des2["mean"]),
                     "count: " + str(des2["count"])))

        # Figure 09:
        # Correlation of price and volume change predictor search
        # TODO
        self.layer_on_top_of_within_currencies.get_volume_price_correlation_cause_search_plot()

        # Stat 10
        # Correlation between age and average market capitalization
        # Stat 11
        # Correlation between age and last market capitalization
        des1, des2 = self.layer_on_top_of_within_currencies.get_age_market_capitalization_correlations()
        data.append((frame_name,
                     "Age and average market capitalization correlation",
                     "correlation: " + str(des1[0]),
                     "p-value: " + str(des1[1])))
        data.append((frame_name,
                     "Age and last market capitalization correlation",
                     "correlation: " + str(des2[0]),
                     "p-value: " + str(des2[1])))

        # Stat 11
        # Correlation between age and average volume
        correlation, p_value = self.layer_on_top_of_within_currencies.get_age_average_volume_correlation()
        data.append((frame_name,
                     "Age and average volume correlation",
                     "correlation: " + str(correlation),
                     "p-value: " + str(p_value)))

        # Figure 10:
        # Slope of linear regression on price
        fig, fig2, fig_name, fig_name2 = self.layer_on_top_of_within_currencies.get_linear_price_regressions_plot()
        fig.savefig(os.path.join(save_path, "Figure10-" + fig_name + ".png"))
        fig2.savefig(os.path.join(save_path, "Figure11-" + fig_name2 + ".png"))

        positives, negatives, positives2, negatives2 = self.layer_on_top_of_within_currencies.get_linear_regression_data()
        data.append((frame_name,
                     "Currencies with positive linear regression slope and interploation limit=1",
                     "positives: " + str(positives)))
        data.append((frame_name,
                     "Currencies with negative linear regression slope and interploation limit=1",
                     "negatives: " + str(negatives)))
        data.append((frame_name,
                     "Currencies with positive linear regression slope and unlimited interpolation",
                     "positives: " + str(positives2)))
        data.append((frame_name,
                     "Currencies with negative linear regression slope and unlimited interpolation",
                     "negatives: " + str(negatives2)))

        # Figure 12, 13:
        # Correlations of volume and price raw data
        self.layer_on_top_of_within_currencies.get_absolute_volume_price_correlation_plot()
        fig, fig2, fig_name, fig_name2 = self.layer_on_top_of_within_currencies.get_absolute_volume_price_correlation_plot()
        fig.savefig(os.path.join(save_path, "Figure12-" + fig_name + ".png"))
        fig2.savefig(os.path.join(save_path, "Figure13-" + fig_name2 + ".png"))

        # Stats:
        # Descriptive statistics of volume and price raw data correlations
        des1, des2 = self.layer_on_top_of_within_currencies.get_absolute_volume_price_correlation_data()
        data.append((frame_name,
                     "Mean of correlation volume and price all",
                     "mean: " + str(des1["mean"]),
                     "count: " + str(des1["count"])))
        data.append((frame_name,
                     "Mean of correlation volume and price only significant ones",
                     "mean: " + str(des2["mean"]),
                     "count: " + str(des2["count"])))

        pprint(data)
