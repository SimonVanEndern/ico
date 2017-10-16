import unittest

import test_commons
from finance.compressed_raw_data.compress_raw_data import SimplifyRawData
from test_commons import TestCommons


class TestSimplifyRawData(unittest.TestCase, TestCommons):

    simplifier = SimplifyRawData()

    def test_aggregate_data(self):
        result = self.simplifier.aggregate_data_from_all_files("bitcoin", only_save_if_not_yet_saved=False)

        regression_file = self.get_test_path()
        self.assertEqual(str(result.to_csv()), test_commons.save_or_compare_data(result.to_csv(), regression_file))



