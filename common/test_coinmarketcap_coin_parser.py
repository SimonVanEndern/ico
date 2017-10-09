import unittest

from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser


class TestCoinmarketcapCoins(unittest.TestCase):
    coinmarketcap_source = CoinmarketCapCoinParser()

    def test_get_coin_data_general(self):
        result = self.coinmarketcap_source.get_all_coins()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 5)

    def test_get_coin_data_sample(self):
        self.coinmarketcap_source.path_to_save = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\common\saved\coinmarketcap-coins2017108.html"
        result = self.coinmarketcap_source.get_all_coins()
        self.assertEqual(result[0], "Bitcoin")
        self.assertEqual(result[9], "Monero")
        self.assertEqual(len(result), 871)


if __name__ == '__main__':
    unittest.main()
