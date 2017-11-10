import unittest
from datetime import datetime
from unittest.mock import patch

import pandas

import test_commons
from common.currency import Currency
from common.currency_handler import CurrencyHandler
from global_data import GlobalData
from test_commons import TestCommons


class CurrencyHandlerTest(unittest.TestCase, TestCommons):
    TestCommons()
    currency_handler = CurrencyHandler.Instance()
    currency_handler.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    GlobalData.last_date_for_download = GlobalData.last_date_for_download2

    def test_get_all_currency_names(self):
        result = self.currency_handler.get_all_currency_names_where_data_is_available()
        self.assertEqual(len(result), 1243)

    def test_add_currency(self):
        result = self.currency_handler.get_currency("bitcoin")
        self.assertEqual(result.currency, "bitcoin")

    def test_add_currency_with_date_limit(self):
        self.currency_handler.get_currency("bitcoin", datetime.strptime("01.01.2016", "%d.%m.%Y"))
        self.currency_handler.get_currency("bitcoin")
        result1: pandas.DataFrame = self.currency_handler.get_currency("bitcoin").data
        result2: pandas.DataFrame = self.currency_handler.get_currency("bitcoin",
                                                                       datetime.strptime("01.01.2016", "%d.%m.%Y")).data

        self.assertEqual(len(result1), 1646)
        self.assertEqual(len(result2), 669)

    def test_get_all_currencies_limited(self):
        self.currency_handler.get_all_currency_names_where_data_is_available()
        result = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=100)
        self.assertEqual(len(result), 100)

    def test_get_basic_currency_data(self):
        result = self.currency_handler.get_basic_currency_data("bitcoin")

        self.assertEqual(result, {"start_date": 1367174841000})

    def test_get_financial_series_start_date_of_all_currencies(self):
        GlobalData.last_date_for_download = GlobalData.last_date_for_download2
        self.currency_handler.load_all_currencies()
        result = self.currency_handler.get_financial_series_start_date_of_all_currencies(limit=10)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_get_all_currency_names_static(self):
        currency_handler = CurrencyHandler.Instance()

        result = currency_handler.get_all_currency_names()

        self.assertEqual(len(result), 1243)

    def test_load_currency_only_ones(self):
        with patch.object(Currency, '__init__', return_value=None) as mock_method:
            currency_handler = CurrencyHandler.Instance()

            currency_handler.get_currency("2give")
            currency_handler.get_currency("2give")

            self.assertLessEqual(mock_method.call_count, 1)
