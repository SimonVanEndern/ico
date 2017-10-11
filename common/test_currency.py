import unittest

from common.currency import Currency


class CurrencyTest(unittest.TestCase):
    ethereum = Currency("ethereum")
    bitcoin = Currency("bitcoin")
    date_limited_currency = Currency("ethereum", date_limit="01.01.2016")

    def reset_limited_currency_to_specific(self):
        self.date_limited_currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.date_limited_currency.instantiate()

    def reset_currency_to_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.instantiate()

    def test_load_data_general(self):
        result = self.ethereum.load_data()
        self.assertGreaterEqual(len(result), 793)
        self.assertEqual(result[0], ['Timestamp', 'USD', 'BTC', 'Volume', 'MarketCap'])

    def test_load_data_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        result = self.ethereum.load_data()
        self.assertEqual(len(result), 793)
        self.assertEqual(result[0], ['Timestamp', 'USD', 'BTC', 'Volume', 'MarketCap'])
        self.assertEqual(result[1], ['1438958970000', '2.83162', '0.0101411', '90621', '0'])

    def test_calculate_daily_return(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_daily_return()
        self.assertEqual(result[:10],
                         [0.0, -0.5300393414370572, -0.46014427954161197, -0.10390123786735472, 0.16572870082281055,
                          0.4578791674439675, 0.31256398069611, 0.5218620521569584, -0.2546957862610788,
                          -0.13430416738292283])

    def test_calculate_rolling_volatility(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_rolling_volatility()
        self.assertEqual(result["30"][:3], [0.20709600699178304, 0.20710665533971717, 0.18275999767266785])
        self.assertEqual(result["90"][:3], [0, 0, 0])
        self.assertEqual(result["180"][180:183], [0.09965761335607827, 0.10070672774496256, 0.10059590110171104])

    def test_calculate_linear_regression_on_volatility(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_linear_regression_on_volatility()
        self.assertEqual(result.slope, -3.2842621099404758e-05)
        self.assertEqual(result.intercept, 0.080459598585799041)

    def test_datapoints_currency(self):
        result = self.ethereum.get_financial_data()
        self.assertEqual(len(result), 792)

    def test_date_limited_currency(self):
        result = self.date_limited_currency.get_financial_data()
        self.assertEqual(len(result), 645)

    def test_beginning_date(self):
        result = self.ethereum.get_beginning_date()
        self.assertEqual(result, 1438958970000)
        result2 = self.bitcoin.get_beginning_date()
        self.assertEqual(result2, 1367174841000)

    def test_get_average_volume(self):
        result = self.bitcoin.calculate_average_volume()
        self.assertEqual(result, 197185423.94779366)
