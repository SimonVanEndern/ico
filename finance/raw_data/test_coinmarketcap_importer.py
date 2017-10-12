import unittest
from unittest.mock import patch

import test_commons
from finance.raw_data.coinmarketcap_importer import CoinmarketcapImportFinanceData
from test_commons import TestCommons


class CoinmarketcapImporterTest(unittest.TestCase, TestCommons):
    coinmarketcap_importer = CoinmarketcapImportFinanceData()

    def test_request_data(self):
        currency = "bitcoin"
        start = 1442458164000
        end = start + 10 * 24 * 3600 * 1000

        result = self.coinmarketcap_importer.request_data(currency, end, start)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_request_data_monthly(self):
        currency = "ethereum"
        start = 1442458164000
        end = start + 40 * 24 * 3600 * 1000

        with patch.object(CoinmarketcapImportFinanceData, 'save_data', return_value=None) as mock_method:
            self.coinmarketcap_importer = CoinmarketcapImportFinanceData()
            self.coinmarketcap_importer.request_data_monthly(currency, start, end)

            self.assertEqual(mock_method.call_count, 2)
