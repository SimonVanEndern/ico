import unittest
import finance.coursedata.financial_data_calculator as fdc


class FinancialDataCalculatorTest(unittest.TestCase):

    def test_calculate_for_timestamp(self):
        result = fdc.calculate_for_timestamp(2, {"time": 1, "data": 1}, {"time": 10, "data": 10})
        self.assertEqual(result, 2)

    def test_calculate_series_for_timestamp(self):
        input_data = [{"time": 1, "data": 5},
                      {"time": 3, "data": 11},
                      {"time": 4, "data": 13}]

        result = fdc.calculate_series_for_timestamp(1, 5, 1, input_data)
        self.assertEqual(result, [(1, 5.0), (2, 8.0), (3, 11.0), (4, 13.0)])
