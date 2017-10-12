import unittest

from ico.matcher import CurrencyNameMatcher


class TestMatcher(unittest.TestCase):
    matcher = CurrencyNameMatcher()

    matcher.currency_map = {"ethereum": "ETH", "bitcoin": "BTC"}
    matcher.currency_map_reverse = {"ETH": "ethereum", "BTC": "bitcoin"}

    def test_match(self):
        input_data = {"ethereum": 300, "Bitcoin": 500, "Test": 0}
        result = self.matcher.match(input_data)

        self.assertEqual(result, {"ETH": 300, "BTC": 500, "test": 0})

    def test_unmatch(self):
        input_data = {"ETH": 300, "BTC": 500, "Test": 0}

        result = self.matcher.unmatch_symbol(input_data)

        self.assertEqual(result, {"ethereum": 300, "bitcoin": 500, "Test": 0})
