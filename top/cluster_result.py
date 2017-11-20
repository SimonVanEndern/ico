from top.calculation_result import CalculationResult


class ClusterResult:
    def __init__(self, result_cluster_1: CalculationResult, result_cluster_2: CalculationResult):
        self.result_cluster_1: CalculationResult = result_cluster_1
        self.result_cluster_2: CalculationResult = result_cluster_2

    def add_cluster_1(self, result_cluster_1: CalculationResult):
        self.result_cluster_1 = result_cluster_1

    def add_cluster_2(self, result_cluster_2: CalculationResult):
        self.result_cluster_2 = result_cluster_2
