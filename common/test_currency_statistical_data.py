import unittest

import test_commons
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from test_commons import TestCommons


class CurrencyStatisticalDataTest(unittest.TestCase, TestCommons):
    TestCommons()
    currency_handler = CurrencyHandler.Instance()
    bitcoin = currency_handler.get_currency("bitcoin")
    statistical_data = CurrencyStatisticalData(bitcoin)

    def test_calculate_total_volume(self):
        result = self.statistical_data.calculate_total_volume()

        self.assertEqual(result, 364934325088.36713)

    def test_calculate_average_volume(self):
        result = self.statistical_data.calculate_average_volume()

        self.assertEqual(result, 221844574.52180374)

    def test_calculate_average_market_capitalization(self):
        result = self.statistical_data.calculate_average_market_capitalization()

        self.assertEqual(result, 12252924752.34539)

    def test_calculate_average_price(self):
        result = self.statistical_data.calculate_average_price()

        self.assertEqual(result, 794.0940216267113)

    def test_calculate_highest_market_capitalization(self):
        result = self.statistical_data.calculate_highest_market_capitalization()

        self.assertEqual(result, 102697965495.76692)

    def test_calculate_highest_price(self):
        result = self.statistical_data.calculate_highest_price()

        self.assertEqual(result, 6166.4713540499997)

    def test_calculate_lowest_price(self):
        result = self.statistical_data.calculate_lowest_price()

        self.assertEqual(result, 68.821236330000005)

    def test_calculate_first_price(self):
        result = self.statistical_data.calculate_first_price()

        self.assertEqual(result, 143.00011122999999)

    def test_calculate_volume_return_correlations(self):
        result = self.statistical_data.calculate_volume_return_correlations()
        print(result)

        for key in [-3, -2, -1, 0, 1, 2, 3]:
            self.assertTrue(str(key) in result)

        self.assertEqual(result, {'0': (0.0066930388624346091, 0.80221762934312513),
                                  '1': (0.029296543577470111, 0.27298432552976915),
                                  '-1': (0.028257174784093213, 0.29037058627241408),
                                  '2': (0.022804893739232075, 0.39369551770111766),
                                  '-2': (-0.065687090789214572, 0.013927607734796905),
                                  '3': (0.015377088373877981, 0.56537379147389366),
                                  '-3': (0.041955495236235166, 0.11662007639399145)}
                         )

    def test_calculate_price_market_capitalization_correlation(self):
        result = self.statistical_data.calculate_price_market_capitalization_correlation()

        self.assertEqual(result, 0.99998736082769446)

    def test_calculate_rolling_volatility(self):
        result = self.statistical_data.calculate_rolling_volatility()

        for key in [30, 90, 180]:
            self.assertTrue(str(key) in result)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_calculate_volume_linreg(self):
        result = self.statistical_data.calculate_volume_linreg()

        self.assertEqual(result.slope, 0.0072956671521211824)
        self.assertEqual(result.intercept, -10271642147.973442)

    def test_calculate_market_capitalization_linreg(self):
        result = self.statistical_data.calculate_market_capitalization_linreg()

        self.assertEqual(result.slope, 0.2640384300139787)

    def test_calculate_usd_linreg(self):
        result = self.statistical_data.calculate_usd_linreg()

        self.assertEqual(result.slope, 1.5189462144348671e-08)
        self.assertEqual(result.intercept, -21053.264194029245)

    def test_calculate_volatility_linreg(self):
        result = self.statistical_data.calculate_volatility_linreg()

        for key in [30, 90, 180]:
            self.assertTrue(str(key) in result)

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

    def test_calculate_fist_date(self):
        result = self.statistical_data.calculate_fist_date()

        self.assertEqual(result, 1367236800000)

    def test_calculate_last_price(self):
        result = self.statistical_data.calculate_last_price()

        self.assertEqual(result, 6166.4713540499997)

    def test_calculate_total_data_points(self):
        result = self.statistical_data.calculate_total_data_points()

        self.assertEqual(result, 1646)

    def test_calculate_price_change_from_beginning(self):
        result = self.statistical_data.calculate_price_change_from_beginning()

        self.assertEqual(result, 43.122143759258392)

    def test_load_google_trends_data(self):
        result = self.statistical_data.load_google_trends_data()

        self.assertEqual(result[:10],
                         [(1356998400, 0.5), (1357084800, 0.0), (1357171200, 0.0), (1357257600, 0.33333333333333326),
                          (1357344000, 0.0), (1357430400, -0.25), (1357516800, 0.0), (1357603200, 0.0),
                          (1357689600, 0.0), (1357776000, 0.0)]
                         )

        print(result[len(result) - 10:])

        self.assertEqual(result[len(result) - 10:],
                         [(1508630400, 0.171875), (1508716800, 0.06666666666666665), (1508803200, -0.09999999999999998),
                          (1508889600, -0.02777777777777779), (1508976000, -0.12857142857142856),
                          (1509062400, -0.1311475409836066), (1509148800, 0.05660377358490565),
                          (1509235200, 0.2142857142857142), (1509321600, 0.16176470588235303),
                          (1509408000, 0.21518987341772156)]
                         )

    def test_calculate_price_correlation_with_google_trends(self):
        result = self.statistical_data.calculate_price_correlation_with_google_trends()

        self.assertEqual(result, ((0.062800655452990239, 0.010844019531653032),
                                  (0.038082906096002976, 0.12259431553104663)))
