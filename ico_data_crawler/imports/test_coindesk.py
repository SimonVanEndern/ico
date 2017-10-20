import os
import sys
import unittest
from datetime import datetime

from ico_data_crawler.imports.coindesk import CoindeskSource


class TestCoindesk(unittest.TestCase):
    coindesk = CoindeskSource()

    def test_get_ico_data_without_currency_map(self):
        self.coindesk.path = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\ico_data_crawler\imports\saved\coindesk2017929.csv"
        self.coindesk.now = datetime.strptime("28.09.2017", "%d.%m.%Y")

        result = self.coindesk.get_ico_data()
        filename = os.path.join(os.path.dirname(__file__), "test_records", sys._getframe().f_code.co_name + ".txt")
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                file.write(str(result))

        with open(filename) as file:
            expected = file.read()

        self.assertEqual(str(result), expected)

    def test_get_ico_data_without_currency_map_new_version(self):
        self.coindesk.path = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\ico_data_crawler\imports\saved\coindesk20171011.csv"
        self.coindesk.now = datetime.now()

        result = self.coindesk.get_ico_data()
        filename = os.path.join(os.path.dirname(__file__), "test_records", sys._getframe().f_code.co_name + ".txt")
        print(filename)
        if not os.path.isfile(filename):
            with open(filename, "w") as file:
                file.write(str(result))

        with open(filename) as file:
            expected = file.read()

        self.assertEqual(str(result), expected)
