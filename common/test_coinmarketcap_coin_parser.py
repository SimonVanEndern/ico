import unittest

from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser


class TestCoinmarketcapCoins(unittest.TestCase):
    coinmarketcap_source = CoinmarketCapCoinParser()

    def test_get_coin_data(self):
        result = self.coinmarketcap_source.get_all_coins()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 5)


if __name__ == '__main__':
    unittest.main()
