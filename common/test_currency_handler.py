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
        self.assertEqual(result.name, "bitcoin")

    def test_add_currency_datapoints(self):
        result = self.currency_handler.get_currency("bitcoin").get_financial_data()
        self.assertEqual(len(result), 1609)

    def test_add_currency_with_date_limit(self):
        self.currency_handler.get_currency("bitcoin", "01.01.2016")
        self.currency_handler.get_currency("bitcoin")
        result1 = self.currency_handler.get_currency("bitcoin").get_financial_data()
        result2 = self.currency_handler.get_currency("bitcoin", "01.01.2016").get_financial_data()

        self.assertEqual(len(result1), 1609)
        self.assertEqual(len(result2), 644)

    def test_get_all_currencies_limited(self):
        self.currency_handler.get_all_currency_names_where_data_is_available()
        result = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=100)
        self.assertEqual(len(result), 100)
