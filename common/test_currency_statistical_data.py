import unittest

import test_commons
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from test_commons import TestCommons


class CurrencyStatisticalDataTest(unittest.TestCase, TestCommons):
    TestCommons()
    currency_handler = CurrencyHandler()
    bitcoin = currency_handler.get_currency("bitcoin")
    statistical_data = CurrencyStatisticalData(bitcoin)

    def test_calculate_total_volume(self):
        result = self.statistical_data.calculate_total_volume()

        self.assertEqual(result, 337449855463.59094)

    def test_calculate_average_volume(self):
        result = self.statistical_data.calculate_average_volume()

        self.assertEqual(result, 206770744.7693572)

    def test_calculate_average_market_capitalization(self):
        result = self.statistical_data.calculate_average_market_capitalization()

        self.assertEqual(result, 11585424962.709578)

    def test_calculate_average_price(self):
        result = self.statistical_data.calculate_average_price()

        self.assertEqual(result, 754.4710237714522)

    def test_calculate_highest_market_capitalization(self):
        result = self.statistical_data.calculate_highest_market_capitalization()

        self.assertEqual(result, 96057813175.93333)

    def test_calculate_highest_price(self):
        result = self.statistical_data.calculate_highest_price()

        self.assertEqual(result, 5776.66577778)

    def test_calculate_lowest_price(self):
        result = self.statistical_data.calculate_lowest_price()

        self.assertEqual(result, 68.46144182)

    def test_calculate_first_price(self):
        result = self.statistical_data.calculate_first_price()

        self.assertEqual(result, 138.47981111)

    def test_calculate_volume_return_correlations(self):
        result = self.statistical_data.calculate_volume_return_correlations()
        print(result)

        for key in [-3, -2, -1, 0, 1, 2, 3]:
            self.assertTrue(str(key) in result)

        self.assertEqual(result, {'0': (0.008747074681059978, 0.74455491874386359),
                                  '1': (0.031672902356229403, 0.23813554503904538),
                                  '-1': (-0.00074715713397255899, 0.97780495656478783),
                                  '2': (0.035638940289499974, 0.18451361244169548),
                                  '-2': (-0.037872455200061543, 0.15847885150672111),
                                  '3': (0.0083249259000856522, 0.75673855708049198),
                                  '-3': (0.012979762277408243, 0.62910805789333457)}
                         )

    def test_calculate_price_market_capitalization_correlation(self):
        result = self.statistical_data.calculate_price_market_capitalization_correlation()

        self.assertEqual(result, 0.99999627711062111)

    def test_calculate_rolling_volatility(self):
        result = self.statistical_data.calculate_rolling_volatility()

        for key in [30, 90, 180]:
            self.assertTrue(str(key) in result)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_calculate_volume_linreg(self):
        result = self.statistical_data.calculate_volume_linreg()

        self.assertEqual(result.slope, 0.0068275558158194423)
        self.assertEqual(result.intercept, -9609539380.8704166)

    def test_calculate_market_capitalization_linreg(self):
        result = self.statistical_data.calculate_market_capitalization_linreg()

        self.assertEqual(result.slope, 0.24176004890900188)

    def test_calculate_usd_linreg(self):
        result = self.statistical_data.calculate_usd_linreg()

        self.assertEqual(result.slope, 1.3854071415722353e-08)
        self.assertEqual(result.intercept, -19164.291295649055)

    def test_calculate_volatility_linreg(self):
        result = self.statistical_data.calculate_volatility_linreg()

        for key in [30, 90, 180]:
            self.assertTrue(str(key) in result)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_calculate_fist_date(self):
        result = self.statistical_data.calculate_fist_date()

        self.assertEqual(result, 1367229600000)

    def test_calculate_last_price(self):
        result = self.statistical_data.calculate_last_price()

        self.assertEqual(result, 5776.6657777800001)

    def test_calculate_total_data_points(self):
        result = self.statistical_data.calculate_total_data_points()

        self.assertEqual(result, 1633)

    def test_calculate_price_change_from_beginning(self):
        result = self.statistical_data.calculate_price_change_from_beginning()

        self.assertEqual(result, 40.714858877091949)
