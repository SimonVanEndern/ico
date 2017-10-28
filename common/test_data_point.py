import unittest

from common.data_point import DataPoint, from_tuple
from test_commons import TestCommons


class DataPointTest(unittest.TestCase, TestCommons):
    def test_sorting(self):
        data_point_1 = DataPoint(3, 2)
        data_point_2 = DataPoint(2, 4)
        data_point_3 = DataPoint(None, 5)

        data_point_list = [data_point_1, data_point_2, data_point_3]

        data_point_list.sort()

        self.assertEqual(data_point_list[0], DataPoint(2, 4))

    def test_get_relative_change(self):
        data_point_1 = DataPoint(1, 3)
        data_point_2 = DataPoint(2, 5)

        relative_change = data_point_1.get_relative_change(data_point_2)

        self.assertEqual(relative_change, 1 - 1 / 3)

    def test_instantiation_from_tuple(self):
        data_point = from_tuple((1, 2))

        expected_result = DataPoint(1, 2)

        self.assertEqual(data_point, expected_result)
