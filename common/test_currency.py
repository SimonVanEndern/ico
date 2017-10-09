import unittest

from common.currency import Currency


class CurrencyTest(unittest.TestCase):
    currency = Currency(extended=True, currency="ethereum")

    def test_load_data_general(self):
        result = self.currency.load_data()
        self.assertGreaterEqual(len(result), 793)
        self.assertEqual(result[0], ['Timestamp', 'USD', 'BTC', 'Volume', 'MarketCap'])

    def test_load_data_specific(self):
        self.currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        result = self.currency.load_data()
        self.assertEqual(len(result), 793)
        self.assertEqual(result[0], ['Timestamp', 'USD', 'BTC', 'Volume', 'MarketCap'])
        self.assertEqual(result[1], ['1438958970000', '2.83162', '0.0101411', '90621', '0'])

    def test_calculate_daily_return(self):
        self.currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.currency.instantiate()
        result = self.currency.calculate_daily_return()
        self.assertEqual(result[:10],
                         [-0.5300393414370572, -0.46014427954161197, -0.10390123786735472, 0.16572870082281055,
                          0.4578791674439675, 0.31256398069611, 0.5218620521569584, -0.2546957862610788,
                          -0.13430416738292283, -0.09388119822988761])
