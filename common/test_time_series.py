import unittest

from common.data_point import DataPoint
from common.time_series import TimeSeries
from test_commons import TestCommons


class TimeSeriesTest(unittest.TestCase, TestCommons):
    def test_initiate_time_series(self):
        data = [(0, 111), (1, 222)]

        time_series = TimeSeries(data)

        time_stamps = time_series.timestamps

        self.assertEqual(time_stamps, [0, 1])

    def test_initiate_with_correct_header(self):
        data = [("timestamp", "data"), (1, 111), (2, 222)]
        expected_data = [(1, 111), (2, 222)]

        time_series = TimeSeries(data)

        expected_result = TimeSeries(expected_data)

        self.assertEqual(time_series, expected_result)

    def test_has_gaps_true(self):
        data = [(0, 111), (1, 222), (2, 333), (4, 4444)]

        time_series = TimeSeries(data)

        has_gaps = time_series.has_gaps(step=1)

        self.assertTrue(has_gaps)

    def test_has_gaps_false(self):
        data = [(0, 111), (1, 222), (2, 333)]

        time_series = TimeSeries(data)

        has_gaps = time_series.has_gaps(step=1)

        self.assertFalse(has_gaps)

    def test_add_data_point(self):
        time_series = TimeSeries(None)

        data_point_1 = DataPoint(1, 2)
        data_point_2 = DataPoint(0, 4)

        time_series.add_data_point(data_point_1)
        time_series.add_data_point(data_point_2)

        expected_data = [(0, 4), (1, 2)]
        expected_result = TimeSeries(expected_data)

        self.assertEqual(expected_result, time_series)

    def test_get_first_timestamp(self):
        data = [(4, 111), (1, 222), (2, 333)]

        time_series = TimeSeries(data)

        self.assertEqual(time_series.get_first_timestamp(), 1)

    def test_number_of_gaps(self):
        data = [(0, 111), (1, 222), (2, 333), (4, 4444), (6, 555), (7, 666)]

        time_series = TimeSeries(data)

        self.assertEqual(time_series.number_of_gaps(step=1), 2)

    def test_number_of_gaps_with_only_one_data_point(self):
        data = [(1, 111)]

        time_series = TimeSeries(data)

        self.assertEqual(time_series.number_of_gaps(step=1), 0)
