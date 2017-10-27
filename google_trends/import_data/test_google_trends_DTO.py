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

        # def test_save_6monthly_data(self):
        #     GlobalData.EXTERNAL_PATH_GOOGLE_TRENDS_DATA = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\google_trends\import_data\\test_input"
        #     GlobalData.RELATIVE_GOOGLE_TRENDS_DATA_PATH = "Z:\Google Drive\\05 - Projekte\\bachelor-thesis\google_trends\import_data\\test_input\\relative"
        #
        #     google_trends_bitcoin = GoogleTrendsDTO("bitcoin")
        #
        #     with patch.object(CSVWriter, "writerow", return_value=False) as csv_writerow_mock:
        #         google_trends_bitcoin.save_6_monthly_data()
        #
        #         csv_writerow_mock.assert_any_call(["Date", "RelativeChange"])
