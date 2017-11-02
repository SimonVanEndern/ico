import csv
import datetime
import logging
import math
from os import path

import matplotlib.pyplot as plt
import pandas

from common.currency_statistical_data import CurrencyStatisticalData
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class Currency:
    data_path = GlobalData.financial_data_path

    def __init__(self, currency, data_path=None, date_limit=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.currency: str = currency
        self.logger.info("Initiating currency {}".format(self.currency))

        self.date_limit = date_limit
        if self.date_limit is not None:
            self.date_limit = datetime.datetime.strptime(date_limit, "%d.%m.%Y")
            self.date_limit = int(self.date_limit.timestamp() * 1e3)

        if data_path is not None:
            self.data_path: str = data_path

        self.data: pandas.DataFrame = None
        self.relative_data: pandas.DataFrame = None

        self.load_financial_data()

        self.maximum_loss = 0

        # self.instantiate()

        self.statistical_data: CurrencyStatisticalData = None

    def get_statistical_data(self):
        self.statistical_data: CurrencyStatisticalData = CurrencyStatisticalData(self)
        return self.statistical_data

    def print(self):
        # TODO: fix if needed
        print("Currency: {} - Gaps: {}".format(self.currency, self.usd.number_of_gaps()))

    def load_financial_data(self) -> None:
        filename = self.currency + str(GlobalData.last_date_for_download) + ".csv"
        filepath = path.join(GlobalData.EXTERNAL_PATH_AGGREGATED_DATA,
                             GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA, self.currency, filename)
        try:
            with open(filepath, "r") as file:
                reader = csv.reader(file)
                self.load_financial_data_from_csv_input(list(reader))
        except FileNotFoundError:
            logging.warning("Currency {} could not be loaded from {}".format(self.currency, filepath))

    def load_financial_data_from_csv_input(self, csv_input: list) -> None:
        if csv_input is None or len(csv_input) < 3:
            raise Exception("Empty csv input")

        header = csv_input.pop(0)
        if header != ["Timestamp", "USD", "BTC", "Volume", "Market_cap"]:
            raise Exception("Wrong file format input")

        # csv_input = list(map(lambda x: ))

        timestamp, usd, btc, volume, market_cap = zip(*csv_input)
        timestamp = list(map(int, timestamp))
        usd = list(map(lambda x: math.nan if x == "" else float(x), usd))
        btc = list(map(lambda x: math.nan if x == "" else float(x), btc))
        volume = list(map(lambda x: math.nan if x == "" else float(x), volume))
        market_cap = list(map(lambda x: math.nan if x == "" else float(x), market_cap))

        if self.date_limit is not None:
            while timestamp[0] < self.date_limit:
                timestamp = timestamp[1:]
                usd = usd[1:]
                volume = volume[1:]
                btc = btc[1:]
                market_cap = market_cap[1:]

        pandas_dict = {"timestamp": timestamp, "usd": usd, "btc": btc, "volume": volume, "market_cap": market_cap}

        self.data = pandas.DataFrame.from_records(pandas_dict, index=timestamp)
        self.relative_data = self.data.interpolate(limit=1).pct_change()

    def print_with_regression(self, data, regression):
        df = pandas.DataFrame(data)
        x_values = range(0, len(data))
        y_values = [regression.slope * i + regression.intercept for i in x_values]
        plt.plot(x_values, y_values, "--")
        plt.plot(df)
        plt.show()

    @staticmethod
    def print_data(data):
        for piece in data:
            df = pandas.DataFrame(piece)
            plt.plot(df)
        plt.show()

    def print_course(self) -> None:
        self.print_with_regression(list(self.data["usd"]), self.price_linear_regression)

    def print_daily_return(self):
        df = pandas.DataFrame(self.daily_return)
        # df2 = pandas.DataFrame(self.volume_relative_change)
        # plt.plot(df2)
        plt.plot(df)
        plt.show()

    def print_volatility(self):
        df = pandas.DataFrame.from_dict(self.volatility)
        df.plot()
        plt.show()

    def print_volume(self):
        self.print_with_regression(list(self.data["volume"]), self.volume_linear_regression)

    def get_financial_data(self):
        return list(self.data["usd"])

    def get_volume_financial_data(self):
        return list(self.data["volume"])

    def print_volume_return_correlations(self):
        for correlation in self.volume_return_correlations:
            print(correlation)

    def is_coin(self):
        # TODO: implement
        pass

    def contains_keyword(self):
        return "coin" in self.currency or "bit" in self.currency or "token" in self.currency
