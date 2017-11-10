import unittest
from datetime import datetime

from common.currency import Currency
from global_data import GlobalData
from test_commons import TestCommons


class CurrencyTest(unittest.TestCase, TestCommons):
    TestCommons()
    # GlobalData.last_date_for_download = GlobalData.TEST_LAST_DATE_FOR_DOWNLOAD
    ethereum = Currency("ethereum")
    bitcoin = Currency("bitcoin")
    iota = Currency("iota")
    date_limited_currency = Currency("ethereum", date_limit=datetime.strptime("01.01.2016", "%d.%m.%Y"))

    def reset_limited_currency_to_specific(self):
        self.date_limited_currency.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.date_limited_currency.instantiate()

    def reset_currency_to_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.instantiate()

    def test_load_data_general(self):
        self.ethereum.load_financial_data()
        result = list(self.ethereum.data["usd"])
        self.assertGreaterEqual(len(result), 793)
        self.assertEqual(result[0], 1.375427)

    def test_load_data_specific(self):
        self.ethereum.data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
        self.ethereum.load_financial_data()
        usd = list(self.ethereum.data["usd"])
        timestamp = self.ethereum.data.index.values[0]
        btc = list(self.ethereum.data["btc"])[0]
        volume = list(self.ethereum.data["volume"])[0]
        market_cap = list(self.ethereum.data["market_cap"])[0]

        self.assertEqual(len(usd), 815)
        self.assertEqual([timestamp, usd[0], btc, volume, market_cap],
                         [1439035200000, 1.375427, 0.0049751500000000002, 168343.0, 82666210.099999994])

    def test_datapoints_currency(self):
        result = self.ethereum.get_financial_data()
        self.assertEqual(len(result), 815)

    def test_date_limited_currency(self):
        result = self.date_limited_currency.get_financial_data()
        self.assertEqual(len(result), 669)

    def test_get_price_correlation(self):
        result = self.bitcoin.get_absolute_price_correlation(self.ethereum)

        self.assertEqual(result, (0.93487762641106409, 0.0))

    def test_get_price_correlation2(self):
        authorship = Currency("authorship")
        bitgold = Currency("bitgold")

        result = authorship.get_absolute_price_correlation(bitgold)

        self.assertEqual(result, (0.11563913578988758, 0.66976489866081823))
