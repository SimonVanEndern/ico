import os
import sys
import unittest
from unittest.mock import patch

from finance.coursedata.coinmarketcap_importer import CoinmarketcapImportFinanceData


class CoinmarketcapImporterTest(unittest.TestCase):
    coinmarketcap_importer = CoinmarketcapImportFinanceData()

    def test_request_data(self):
        currency = "bitcoin"
        start = 1442458164000
        end = start + 10 * 24 * 3600 * 1000

        result = self.coinmarketcap_importer.request_data(currency, end, start)

        self.assertEqual(str(result), self.save_or_compare_data(result))

    def test_request_data_monthly(self):
        currency = "ethereum"
        start = 1442458164000
        end = start + 40 * 24 * 3600 * 1000

        with patch.object(CoinmarketcapImportFinanceData, 'save_data', return_value=None) as mock_method:
            self.coinmarketcap_importer = CoinmarketcapImportFinanceData()
            self.coinmarketcap_importer.request_data_monthly(currency, start, end)

            self.assertEqual(mock_method.call_count, 2)

    @staticmethod
    def save_or_compare_data(data):
        filename = os.path.join(os.path.dirname(__file__), "test_records", sys._getframe().f_code.co_name + ".txt")
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                file.write(str(data))

        with open(filename) as file:
            expected = file.read()
            return expected
