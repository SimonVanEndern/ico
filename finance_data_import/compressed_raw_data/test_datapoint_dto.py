import unittest

from finance_data_import.compressed_raw_data.datapoint_dto import DatapointDTO


class DatapointDTOTEst(unittest.TestCase):
    def test_relaxed_comparison(self):
        datapoint_1 = DatapointDTO(1, 2, 3, 4, 5)
        datapoint_2 = DatapointDTO(1, 2, 3, 4, 5)
        datapoint_3 = DatapointDTO(1, 2, 3, 4, 0)
        datapoint_4 = DatapointDTO(1, 2, 3, 4, 8)

        self.assertTrue(datapoint_1.compare_relaxed(datapoint_2))
        self.assertTrue(datapoint_1.compare_relaxed(datapoint_3))
        self.assertFalse(datapoint_1.compare_relaxed(datapoint_4))
        self.assertTrue(datapoint_3.compare_relaxed(datapoint_4))
