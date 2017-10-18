import csv
import unittest

from finance.analysis import calculate_average_volume


class CoinmarketStartTimeTest(unittest.TestCase):

    def test_calculate_average_volume(self):
        testpath = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\allion.csv"
        test_input = None
        with open(testpath) as file:
            reader = csv.reader(file)
            test_input = list(reader)

        result = calculate_average_volume(test_input)
        self.assertEqual(result, 607.65549132947979)
