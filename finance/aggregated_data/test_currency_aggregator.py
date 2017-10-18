import unittest

import test_commons
from finance.aggregated_data.currency_aggregator import CurrencyAggregator
from global_data import GlobalData
from test_commons import TestCommons


class CurrencyAggregatorTest(unittest.TestCase, TestCommons):
    pass
    # def test_aggregate_currency(self):
    #     GlobalData.EXTERNAL_PATH_COMPRESSED_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\finance\\aggregated_data\\test_input\compressed-data"
    #     GlobalData.EXTERNAL_PATH_AGGREGATED_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\finance\\aggregated_data\\test_input\\final_aggregated_data"
    #     self.currency_aggregator = CurrencyAggregator("bitcoin", GlobalData.last_date_for_download)
    #
    #     result = self.currency_aggregator.aggregate_currency()
    #
    #     regression_file = self.get_test_path()
    #     self.assertEqual(str(result.to_csv()), test_commons.save_or_compare_data(result.to_csv(), regression_file))

