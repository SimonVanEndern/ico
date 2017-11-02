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

        for key in [-3, -2, -1, 0, 1, 2, 3]:
            self.assertTrue(str(key) in result)

        self.assertEqual(result, {'0': (0.017420617789105777, 0.51652017436179753),
                                  '1': (0.00058970434776113296, 0.98248771425952008),
                                  '-1': (0.0053032089137628772, 0.84351526919049757),
                                  '2': (0.018636680319309731, 0.48798951203124197),
                                  '-2': (-0.034105939092749074, 0.20429387692658899),
                                  '3': (-0.005436847637652965, 0.83973896453692498),
                                  '-3': (-0.004709099046997468, 0.86095553236827072)}
                         )

    def test_calculate_price_market_capitalization_correlation(self):
        result = self.statistical_data.calculate_price_market_capitalization_correlation()

        self.assertEqual(result, 0.99999627052346574)

    def test_calculate_rolling_volatility(self):
        result = self.statistical_data.calculate_rolling_volatility()

        for key in [30, 90, 180]:
            self.assertTrue(str(key) in result)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_calculate_volume_linreg(self):
        result = self.statistical_data.calculate_volume_linreg()

        self.assertEqual(result.slope, 0.0068279411817183423)
        self.assertEqual(result.intercept, -9609958904.9467716)

    def test_calculate_market_capitalization_linreg(self):
        result = self.statistical_data.calculate_market_capitalization_linreg()

        self.assertEqual(result.slope, 0.24177646112090923)

    def test_calculate_usd_linreg(self):
        result = self.statistical_data.calculate_usd_linreg()

        self.assertEqual(result.slope, 1.3855105113996949e-08)
        self.assertEqual(result.intercept, -19165.416619179541)

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

        self.assertEqual(result, 1632)

    def test_calculate_price_change_from_beginning(self):
        result = self.statistical_data.calculate_price_change_from_beginning()

        self.assertEqual(result, 40.714858877091949)
