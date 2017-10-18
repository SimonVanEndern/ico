import json
import unittest

import test_commons
from finance_data_import.compressed_raw_data.currency_dto import CurrencyDTO
from test_commons import TestCommons


class TestCurrencyDTO(unittest.TestCase, TestCommons):

    currency_dto = CurrencyDTO("bitcoin")
    sample_file_path = "X:\\bachelor-thesis\data\\bitcoin\\1367174841000-1369680441000.json"

    def test_to_csv(self):
        with open(self.sample_file_path) as file:
            data = json.load(file)
            self.currency_dto.add_data(data)
            result = self.currency_dto.to_csv()

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))

