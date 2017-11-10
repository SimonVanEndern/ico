import unittest
from typing import List
from unittest.mock import MagicMock

from finance_data_import.aggregated_data.currency_aggregator import CurrencyAggregator
from test_commons import TestCommons


class CurrencyAggregatorTest(unittest.TestCase, TestCommons):
    currency_aggregator = CurrencyAggregator("test", None)

    # def test_aggregate_currency(self):
    #     GlobalData.EXTERNAL_PATH_COMPRESSED_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\finance\\aggregated_data\\test_input\compressed-data"
    #     GlobalData.EXTERNAL_PATH_AGGREGATED_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\finance\\aggregated_data\\test_input\\final_aggregated_data"
    #     self.currency_aggregator = CurrencyAggregator("bitcoin", GlobalData.last_date_for_download)
    #
    #     result = self.currency_aggregator.aggregate_currency()
    #
    #     regression_file = self.get_test_path()
    #     self.assertEqual(str(result.to_csv()), test_commons.save_or_compare_data(result.to_csv(), regression_file))

    def test_aggregate_data(self):
        self.currency_aggregator.fdc.get_missing_data = MagicMock()
        input_data = [("Timestamp", "USD", "BTC", "Volume", "Market_cap"),
                      (1.38814E+12, 753.1799333, 1, 63813562.18, 9174025275),
                      (1.38822E+12, 734.6613333, 1, 37592870.89, 8951545823),
                      (1.38831E+12, 721.4994778, 1, 27287725, 8793995161),
                      (1.3884E+12, 750.8261179, 1, 22945155.28, 9152514065)]

        input_data.pop(0)
        result = self.currency_aggregator.aggregate_data(input_data)

        self.assertEqual(result, [[1388145600000, 751.8836313, 1.0, 61978113.7897, 9158451713.36],
                                  [1388232000000, None, None, None, None, None]])
        self.assertTrue(isinstance(result, list))
