import unittest

from common.currency_handler import CurrencyHandler


class CurrencyHandlerTest(unittest.TestCase):
    currency_handler = CurrencyHandler()
    currency_handler.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"

    def test_get_all_currency_names(self):
        result = self.currency_handler.get_all_currency_names_where_data_is_available()
        self.assertEqual(len(result), 1148)

    def test_add_currency(self):
        result = self.currency_handler.get_currency("bitcoin")
        self.assertEqual(result.currency, "bitcoin")

    def test_add_currency_datapoints(self):
        result = self.currency_handler.get_currency("bitcoin").get_financial_data()
        self.assertEqual(len(result), 1616)

    def test_add_currency_with_date_limit(self):
        self.currency_handler.get_currency("bitcoin", "01.01.2016")
        self.currency_handler.get_currency("bitcoin")
        result1 = self.currency_handler.get_currency("bitcoin").get_financial_data()
        result2 = self.currency_handler.get_currency("bitcoin", "01.01.2016").get_financial_data()

        self.assertEqual(len(result1), 1616)
        self.assertEqual(len(result2), 647)

    def test_get_all_currencies_limited(self):
        self.currency_handler.get_all_currency_names_where_data_is_available()
        result = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=100)
        self.assertEqual(len(result), 100)

    def test_get_basic_currency_data(self):
        result = self.currency_handler.get_basic_currency_data("bitcoin")

        self.assertEqual(result, {"start_date": 1367174841000})
