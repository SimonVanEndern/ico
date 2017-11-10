import os
import unittest
from datetime import datetime
from unittest.mock import patch, MagicMock, mock_open

import test_commons
from finance_data_import.raw_data.coinmarketcap_importer import CoinMarketCapGraphAPIImporter
from global_data import GlobalData
from test_commons import TestCommons


class CoinmarketcapImporterTest(unittest.TestCase, TestCommons):
    TestCommons()
    coinmarketcap_importer = CoinMarketCapGraphAPIImporter()

    def test_request_data(self):
        currency = "bitcoin"
        start = 1442458164000
        end = start + 10 * 24 * 3600 * 1000

        result = self.coinmarketcap_importer.request_data(currency, end, start, "")

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_request_data_monthly(self):
        currency = "ethereum"
        start = 1442458164000
        end = start + 40 * 24 * 3600 * 1000

        with patch.object(CoinMarketCapGraphAPIImporter, 'save_data', return_value=None) as mock_save_data:
            self.coinmarketcap_importer = CoinMarketCapGraphAPIImporter()
            self.coinmarketcap_importer.request_data = MagicMock()
            self.coinmarketcap_importer.request_data_monthly(currency, start, end)

            self.assertEqual(mock_save_data.call_count, 2)
            self.assertEqual(self.coinmarketcap_importer.request_data.call_count, 2)
            self.coinmarketcap_importer.request_data.assert_any_call(currency, 1442458164000, 1444963764000,
                                                                        GlobalData.EXTERNAL_PATH_RAW_DATA)
            self.coinmarketcap_importer.request_data.assert_any_call(currency, 1444963764000, 1445914164000,
                                                                        GlobalData.EXTERNAL_PATH_RAW_DATA)

    def test_request_currency(self):
        currency = "ripple"
        last_date = GlobalData.LAST_DATA_FOR_DOWNLOAD

        with patch('os.path.isfile', return_value=False) as is_file_mock:
            self.coinmarketcap_importer.request_data_monthly = MagicMock(name="request_data_monthly")
            self.coinmarketcap_importer.currency_handler.get_basic_currency_data = MagicMock(
                return_value={'start_date': 1375642265000})
            with patch('builtins.open', mock_open(read_data="data")) as open_mock:
                self.coinmarketcap_importer.request_currency(currency, last_date)

                is_file_mock.assert_called_once_with(
                    os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, currency, "ready" + str(last_date)))
                self.coinmarketcap_importer.request_data_monthly.assert_called_once()
                open_mock.assert_called_once_with(
                    os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, currency, "ready" + str(last_date)),
                    "w")
