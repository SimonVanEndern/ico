import unittest

from finance.aggregate_compressed_data import financial_data_calculator
from finance.aggregate_compressed_data.financial_data_calculator import FinancialDataCalculator


class FinancialDataCalculatorTest(unittest.TestCase):

    fdc = FinancialDataCalculator()

    def test_calculate_for_timestamp(self):
        input_data = [{'time': 1, 'data': [100, 1, 0, 150]},
                      {'time': 9, 'data': [120, 2, 0, 140]}]
        expected_output = {'time': 5, 'data': [110.0, 1.5, 0.0, 145.0]}
        result = self.fdc.calculate_for_timestamp(5, input_data[0], input_data[1])
        self.assertEqual(result, expected_output)

    def test_calculate_For_timestamp_2(self):
        input_data = [{"time": 1, "data": [5]},
                      {"time": 3, "data": [11]}]

        expected_output = {'time': 2, "data": [8.0]}

        result = self.fdc.calculate_for_timestamp(2, input_data[0], input_data[1])
        self.assertEqual(result, expected_output)

    def test_calculate_series_for_timestamp(self):
        input_data = [{"time": 1, "data": [5]},
                      {"time": 3, "data": [11]},
                      {"time": 4, "data": [13]}]

        expected_result = [{'time': 1, "data": [5.0]},
                           {'time': 2, "data": [8.0]},
                           {'time': 3, "data": [11.0]},
                           {'time': 4, "data": [13.0]}]

        result = self.fdc.calculate_series_for_timestamp(1, 5, 1, input_data)
        self.assertEqual(result, expected_result)

    def test_get_next_timestamp_at_time(self):
        input_data = 1454963764000
        input_data2 = 1455003300000
        result = financial_data_calculator.get_next_timestamp_at_time(input_data, 12)
        result2 = financial_data_calculator.get_next_timestamp_at_time(input_data2, 12)

        self.assertEqual(result, 1455015600000)
        self.assertEqual(result2, 1455015600000)

    def test_get_last_timestamp_at_time(self):
        input_data = 1454963764000
        input_data2 = 1455003300000
        result = financial_data_calculator.get_last_timestamp_at_time(input_data, 12)
        result2 = financial_data_calculator.get_last_timestamp_at_time(input_data2, 12)

        self.assertEqual(result, 1454929200000)
        self.assertEqual(result2, 1454929200000)
