from typing import Dict, Tuple

from top.calculation_result import CalculationResult


class ClusterResultContainer:

    def __init__(self, time_frame):
        self.time_frame = time_frame
        self.clustered_results: Dict[str, Tuple[CalculationResult, CalculationResult]]
