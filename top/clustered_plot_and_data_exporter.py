import matplotlib.pyplot as plt

from top.calculation_result import CalculationResult
from top.cluster_result_container import ClusterResultContainer
from top.plot_and_data_exporter import StatisticalAnalysisRunnerAndExporter
from top.statistical_analysis_calculator import StatisticalAnalysisCalculator


class ClusteredStatisticalAnalysisRunnerAndExporter(StatisticalAnalysisRunnerAndExporter):
    def __init__(self, name, data_cluster_1, data_cluster_2, subfolder=None):
        super().__init__(name, data_cluster_1, subfolder=subfolder)
        self.original_data_1: dict = data_cluster_1
        self.original_data_2: dict = data_cluster_2
        self.sac: StatisticalAnalysisCalculator = StatisticalAnalysisCalculator(data_cluster_1)
        self.sac_1: StatisticalAnalysisCalculator = StatisticalAnalysisCalculator(data_cluster_1)
        self.sac_2: StatisticalAnalysisCalculator = StatisticalAnalysisCalculator(data_cluster_2)

        self.data_to_export = ClusterResultContainer(self.frame_name, subfolder)

        self.name_cluster_1 = subfolder + " lower half"
        self.name_cluster_2 = subfolder + " upper half"

    def save_plot(self, func) -> None:
        fig, ax = plt.subplots()
        fig.set_size_inches(7, 3.5)

        fig, ax, fig_name = func(fig=fig, ax=ax, multiple=False, legend_name=self.name_cluster_1)
        self.sac.data = self.sac_2.data
        fig, ax, fig_name = func(fig=fig, ax=ax, multiple=True, legend_name=self.name_cluster_2)
        self.sac.data = self.sac_1.data

        fig.canvas.set_window_title("Figure " + str(self.figure_counter))

        self.save_figure(fig, fig_name)

    def save_plots(self, func) -> None:
        fig1, fig2, fig_name1, fig_name2 = func()
        fig1.set_size_inches(7, 3.5)
        fig2.set_size_inches(7, 3.5)

        fig1.canvas.set_window_title("Figure " + str(self.figure_counter))
        fig2.canvas.set_window_title("Figure " + str(self.figure_counter))

        self.save_figure(fig1, fig_name1)
        self.save_figure(fig2, fig_name2)

    def add_mean_and_count_data_multiple(self, name1, name2, func) -> None:
        des1, des2 = func()
        self.data.append((self.frame_name, name1, "mean: " + str(des1["mean"]), "count: " + str(des1["count"])))
        self.data.append((self.frame_name, name2, "mean: " + str(des2["mean"]), "count: " + str(des2["count"])))

        result = CalculationResult(name1, "mean", des1["mean"], "count", des1["count"])
        result2 = CalculationResult(name2, "mean", des2["mean"], "count", des2["count"])
        self.data_to_export.add_result(result, name1)
        self.data_to_export.add_result(result2, name2)

        self.sac.data = self.sac_2.data

        des1, des2 = func()
        self.data.append((self.frame_name, name1, "mean: " + str(des1["mean"]), "count: " + str(des1["count"])))
        self.data.append((self.frame_name, name2, "mean: " + str(des2["mean"]), "count: " + str(des2["count"])))

        result = CalculationResult(name1, "mean", des1["mean"], "count", des1["count"])
        result2 = CalculationResult(name2, "mean", des2["mean"], "count", des2["count"])
        self.data_to_export.add_result(result, name1)
        self.data_to_export.add_result(result2, name2)

        self.sac.data = self.sac_1.data

    def add_descriptive_data(self, result_name, func: Callable) -> None:
        result = CalculationResult(result_name, name_value_dict=func())
        self.data_to_export.add_result(result, result_name)

        self.sac.data = self.sac_2.data

        result = CalculationResult(result_name, name_value_dict=func())
        self.data_to_export.add_result(result, result_name)

        self.sac.data = self.sac_1.data
