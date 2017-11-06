import unittest
from unittest.mock import patch

from finance_data_import.raw_data.coinmarketcap_importer import CoinMarketCapGraphAPIImporter
from finance_data_import.raw_data.raw_data_importer import RawDataImporter
from test_commons import TestCommons


class RawDataImporterTest(unittest.TestCase, TestCommons):
    TestCommons()
    raw_data_importer = RawDataImporter()

    def test_download_all_data(self):
        with patch.object(CoinMarketCapGraphAPIImporter, "request_currency", return_value=None) as mock_method:
            self.raw_data_importer.coinmarketcap_importer = CoinMarketCapGraphAPIImporter()
            self.raw_data_importer.download_all_data()

            self.assertEqual(mock_method.call_count, 1243)
