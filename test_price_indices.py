import unittest

from price_indices import PriceIndices


class TestPriceIndices(unittest.TestCase):
    def test_calculate_weights(self):
        price_indices = PriceIndices()

        input = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 9, 10: 9, 11: 6, 12: 18, 13: 40, 14: 50, 15: 50}

        result = price_indices.calculate_weights(input, .2)

        expected_output = {1: 0.005128205128205129, 2: 0.010256410256410258, 3: 0.015384615384615385,
                           4: 0.020512820512820516, 5: 0.025641025641025644, 6: 0.03076923076923077,
                           7: 0.0358974358974359, 8: 0.04102564102564103, 9: 0.046153846153846156,
                           10: 0.046153846153846156, 11: 0.03076923076923077, 12: 0.09230769230769231, 13: 0.2, 14: 0.2,
                           15: 0.2}

        self.assertEqual(result, expected_output)

    def test_calculate_weights_2(self):
        price_indices = PriceIndices()

        input = {'0x': 0, '10mtoken': 0, '1337coin': 0, '1credit': 0, '2give': 0, '300-token': 0,
                 '42-coin': 155784.12087911999, '808coin': 0, '8bit': 0, '9coin': 0, 'bitcoin': 8789760047.2000008}

        result = price_indices.calculate_weights(input, .2)

        expected_output = {'0x': 0.0, '10mtoken': 0.0, '1337coin': 0.0, '1credit': 0.0, '2give': 0.0, '300-token': 0.0,
                           '42-coin': 0.5, '808coin': 0.0, '8bit': 0.0, '9coin': 0.0, 'bitcoin': 0.5}

        self.assertEqual(result, expected_output)
