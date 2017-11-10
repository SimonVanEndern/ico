import unittest

import test_commons
from global_data import GlobalData
from google_trends.import_data.google_trends_DTO import GoogleTrendsDTO
from test_commons import TestCommons


class GoogleTrendsDTOTest(unittest.TestCase, TestCommons):
    def test_load_6monthly_data(self):
        GlobalData.EXTERNAL_PATH_GOOGLE_TRENDS_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\google_trends\import_data\\test_input"
        google_trends_bitcoin = GoogleTrendsDTO("bitcoin")

        result = google_trends_bitcoin.relative_change_6monthly
        print(str(result))

        regression_file = self.get_test_path()
        self.assertEqual(str(result), test_commons.save_or_compare_data(result, regression_file))
