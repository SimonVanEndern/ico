import csv
import os
from typing import Dict

from top.calculation_result import CalculationResult
from top.cluster_result import ClusterResult


class ClusterResultContainer:
    def __init__(self, time_frame, clustering_name):
        self.time_frame = time_frame
        self.clustering_name = clustering_name
        self.clustered_results: Dict[str, ClusterResult] = dict()

    def add_result(self, result: CalculationResult, name: str):
        if name not in self.clustered_results:
            self.clustered_results[name] = ClusterResult(result, None)
        else:
            clustered_result = self.clustered_results[name]
            if clustered_result.result_cluster_1 is None:
                clustered_result.add_cluster_1(result)
            else:
                clustered_result.add_cluster_2(result)

    def save(self, save_path):
        with open(os.path.join(save_path, self.clustering_name + ".csv"), "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow([self.time_frame])
            writer.writerow(["Result name", "Cluster1 Value1", "Cluster1 Value2", "Cluster2 Value1, Cluster2 Value2"])

            for result_name in self.clustered_results:
                result = self.clustered_results[result_name]
                if result.result_cluster_1.name_value_dict is not None:
                    writer.writerow([result_name] + list(result.result_cluster_1.name_value_dict.keys()))
                    writer.writerow(["cluster1"] + list(result.result_cluster_1.name_value_dict.values()))
                    if result.result_cluster_2 is not None and result.result_cluster_2.name_value_dict is not None:
                        writer.writerow(["cluster2"] + list(result.result_cluster_2.name_value_dict.values()))
                else:
                    writer.writerow([result_name,
                                     result.result_cluster_1.name_value_1 if result.result_cluster_1 is not None else "",
                                     result.result_cluster_1.name_value_2 if result.result_cluster_1 is not None else "",
                                     result.result_cluster_2.name_value_1 if result.result_cluster_2 is not None else "",
                                     result.result_cluster_2.name_value_2 if result.result_cluster_2 is not None else ""])

                    writer.writerow(["", result.result_cluster_1.value_1 if result.result_cluster_1 is not None else "",
                                     result.result_cluster_1.value_2 if result.result_cluster_1 is not None else "",
                                     result.result_cluster_2.value_1 if result.result_cluster_2 is not None else "",
                                     result.result_cluster_2.value_2 if result.result_cluster_2 is not None else ""])
