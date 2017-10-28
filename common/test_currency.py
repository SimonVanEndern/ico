import unittest

from common.currency import Currency
from global_data import GlobalData
from test_commons import TestCommons


class CurrencyTest(unittest.TestCase, TestCommons):
    TestCommons()
    GlobalData.last_date_for_download = GlobalData.TEST_LAST_DATE_FOR_DOWNLOAD
    ethereum = Currency("ethereum")
    bitcoin = Currency("bitcoin")
    iota = Currency("iota")
    date_limited_currency = Currency("ethereum", date_limit="01.01.2016")

    def reset_limited_currency_to_specific(self):
        self.date_limited_currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.date_limited_currency.instantiate()

    def reset_currency_to_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.instantiate()

    def test_load_data_general(self):
        self.ethereum.load_financial_data()
        result = self.ethereum.usd.data
        self.assertGreaterEqual(len(result), 793)
        self.assertEqual(result[0], 0.42983386)

    def test_load_data_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.load_financial_data()
        result = self.ethereum.usd.data
        self.assertEqual(len(result), 795)
        self.assertEqual(result[0], ['Timestamp', 'USD', 'BTC', 'Volume', 'Market_cap'])
        self.assertEqual(result[1], ['1439028000000', '1.52', '0.01', '152450.6', '91181131.3'])

    def test_calculate_daily_return(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_daily_return()
        print(result[:10])
        self.assertEqual(result[:10],
                         [0.0, -0.5, -0.0921052631578948, 0.01449275362318847, 0.5571428571428574, 0.11009174311926584,
                          0.6033057851239669, -0.10824742268041232, -0.34104046242774566, 0.26315789473684226])

    def test_calculate_rolling_volatility(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_rolling_volatility()
        self.assertEqual(result["30"][:3], [0.20292184418490028, 0.20336324932654237, 0.17964339865288145])
        self.assertEqual(result["90"][:3], [0, 0, 0])
        self.assertEqual(result["180"][180:183], [0.083490658036123683, 0.084348686513140134, 0.08439131962991514])

    def test_calculate_linear_regression_on_volatility(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_linear_regression_on_volatility()
        self.assertEqual(result.slope, -2.4068307700859662e-06)
        self.assertEqual(result.intercept, 0.068685488465432029)

    def test_datapoints_currency(self):
        result = self.ethereum.get_financial_data()
        self.assertEqual(len(result), 794)

    def test_date_limited_currency(self):
        result = self.date_limited_currency.get_financial_data()
        self.assertEqual(len(result), 647)

    def test_beginning_date(self):
        result = self.ethereum.get_beginning_date()
        self.assertEqual(result, 1439028000000)
        result2 = self.bitcoin.get_beginning_date()
        self.assertEqual(result2, 1367229600000)

    def test_get_average_volume(self):
        result = self.bitcoin.calculate_average_volume()
        self.assertEqual(result, 198872446.26214108)

    def test_get_highest_market_capitalization(self):
        result = self.bitcoin.calculate_highest_market_capitalization()

        self.assertEqual(result, 79561291314.17)

    def test_get_highest_market_capitalization_iota(self):
        result = self.iota.calculate_highest_market_capitalization()

        self.assertEqual(result, 2999824943.86)

    def test_calculate_volume_average(self):
        result = self.bitcoin.calculate_volume_average()

        self.assertEqual(result, 198872446.26214108)
