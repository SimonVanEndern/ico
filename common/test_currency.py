import unittest

import pandas

from common.currency import Currency
from global_data import GlobalData
from test_commons import TestCommons


class CurrencyTest(unittest.TestCase, TestCommons):
    TestCommons()
    GlobalData.last_date_for_download = GlobalData.TEST_LAST_DATE_FOR_DOWNLOAD
    ethereum = Currency("ethereum")
    bitcoin = Currency("bitcoin")
    iota = Currency("iota")
    date_limited_currency = Currency("ethereum", date_limit="01.01.2016")

    def reset_limited_currency_to_specific(self):
        self.date_limited_currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.date_limited_currency.instantiate()

    def reset_currency_to_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.instantiate()

    def test_load_data_general(self):
        self.ethereum.load_financial_data()
        result = self.ethereum.usd.data
        self.assertGreaterEqual(len(result), 793)
        self.assertEqual(result[0], 1.517101)

    def test_load_data_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.load_financial_data()
        usd = self.ethereum.usd.data
        timestamp = self.ethereum.usd.timestamps[0]
        btc = self.ethereum.btc.data[0]
        volume = self.ethereum.volume.data[0]
        market_cap = self.ethereum.market_cap.data[0]

        self.assertEqual(len(usd), 802)
        self.assertEqual([timestamp, usd[0], btc, volume, market_cap],
                         [1439028000000, 1.517101, 0.00545335, 152450.6, 91181131.3])

    def test_calculate_daily_return(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_daily_return().fillna(value=0)
        small_result = list(result[result.columns[0]])
        self.assertEqual(small_result[:10],
                         [0.0, -0.50213923133660843, -0.09189316046825946, 0.017169236753527439, 0.5595622419891102,
                          0.11504068654506083, 0.5963260002184565, -0.10513995468531823, -0.34028711503221143,
                          0.26007442226847943])

    def test_calculate_rolling_volatility_30(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_rolling_volatility()
        result_30 = result["30"]
        result_30 = list(result_30[result_30.columns[0]])[30:33]
        self.assertEqual(result_30, [0.20611584804867955, 0.18168399987149483, 0.18066589678214334])

    def test_calculate_rolling_volatility_90(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_rolling_volatility()
        result_90 = result["90"].fillna(value=0)
        result_90 = list(result_90[result_90.columns[0]])[60:63]

        self.assertEqual(result_90, [0, 0, 0])

    def test_calculate_rolling_volatility_180(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_rolling_volatility()
        result_180 = result["180"]
        result_180 = list(result_180[result_180.columns[0]])[180:183]

        self.assertEqual(result_180, [0.10584546743789451, 0.09869581984006992, 0.098416361641586778])

    def test_calculate_linear_regression_on_volatility(self):
        self.reset_currency_to_specific()
        result = self.ethereum.calculate_linear_regression_on_volatility()
        self.assertEqual(result.slope, -1.6000007493874831e-06)
        self.assertEqual(result.intercept, 0.069254709039220624)

    def test_datapoints_currency(self):
        result = self.ethereum.get_financial_data()
        self.assertEqual(len(result), 802)

    def test_date_limited_currency(self):
        result = self.date_limited_currency.get_financial_data()
        self.assertEqual(len(result), 656)

    def test_beginning_date(self):
        result = self.ethereum.get_beginning_date()
        self.assertEqual(result, 1439028000000)
        result2 = self.bitcoin.get_beginning_date()
        self.assertEqual(result2, 1367229600000)

    def test_get_highest_market_capitalization(self):
        result = self.bitcoin.calculate_highest_market_capitalization()

        self.assertEqual(result, 96057813175.93333)

    def test_get_highest_market_capitalization_iota(self):
        result = self.iota.calculate_highest_market_capitalization()

        self.assertEqual(result, 2999824943.855876)

    def test_calculate_volume_average(self):
        result = self.bitcoin.calculate_volume_average()

        self.assertEqual(result, 206770744.7693572)

    def test_calculate_volume_return_correlation(self):
        result = self.bitcoin.calculate_volume_return_correlation()

        self.assertEqual(result, 0.017299315110373175)

    def test_calculate_linear_regression(self):
        df = pandas.DataFrame([1, 2, 3, None, 5, 6])
        df = df.interpolate(limit=1)
        print(df)

        result = self.bitcoin.calculate_linear_regresseion(df)

        self.assertEqual(result.slope, 1.0)
        self.assertEqual(result.intercept, 1.0)
