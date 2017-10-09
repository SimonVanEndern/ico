import unittest

from common.coinmarketcap_token_parser import CoinmarketCapTokenParser


class TestCoinmarketcapTokens(unittest.TestCase):
    coinmarketcap_source = CoinmarketCapTokenParser()

    def test_get_coin_data(self):
        result = self.coinmarketcap_source.get_all_tokens()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 5)


if __name__ == '__main__':
    unittest.main()
