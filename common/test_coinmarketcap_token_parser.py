import unittest

from common.coinmarketcap_token_parser import CoinmarketCapTokenParser


class TestCoinmarketcapTokens(unittest.TestCase):
    coinmarketcap_source = CoinmarketCapTokenParser()

    def test_get_coin_data(self):
        result = self.coinmarketcap_source.get_all_tokens()
        self.assertIsInstance(result, list)
        self.assertGreater(len(result), 5)

    def test_get_coin_data_sample(self):
        self.coinmarketcap_source.path_to_save = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\common\saved\coinmarketcap-tokens2017108.html"
        result = self.coinmarketcap_source.get_all_tokens()
        self.assertEqual(result[0]["currency"], "omisego")
        self.assertEqual(result[0]["platform"], "Ethereum")
        self.assertEqual(result[9]["currency"], "maidsafecoin")
        self.assertEqual(result[9]["platform"], "Omni")
        self.assertEqual(len(result), 277)


if __name__ == '__main__':
    unittest.main()
