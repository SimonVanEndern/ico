import csv
import datetime
import logging
from os import path

import matplotlib.pyplot as plt
import numpy
import pandas
from scipy import stats

from common.calculations import calculate_linear_regression
from common.currency_statistical_data import CurrencyStatisticalData
from common.time_series import TimeSeries
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class Currency:
    data_path = GlobalData.financial_data_path

    def __init__(self, currency, data_path=None, date_limit=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.logger.info("Initiating currency {}".format(self.currency))

        self.date_limit = date_limit
        if self.date_limit is not None:
            self.date_limit = datetime.datetime.strptime(date_limit, "%d.%m.%Y")
            self.date_limit = int(self.date_limit.timestamp() * 1e3)

        if data_path is not None:
            self.data_path: str = data_path

        self.currency: str = currency

        # Inputs
        self.usd: TimeSeries = None
        self.btc: TimeSeries = None
        self.market_cap: TimeSeries = None
        self.volume: TimeSeries = None

        self.load_financial_data()

        # self.start_date: int = self.calculate_start_date()

        self.price_linear_regression = None
        self.volume_linear_regression = None
        self.volume_return_correlations = None
        self.volume_relative_change = None

        self.maximum_loss = 0
        self.gain_over_total_listing_period = 0

        self.data: pandas.DataFrame = None
        self.relative_data: pandas.DataFrame = None

        self.instantiate()

        self.statistical_data = CurrencyStatisticalData(self)

    def instantiate(self):
        self.logger.info("Initiating currency {}".format(self.currency))

        self.price_linear_regression = calculate_linear_regression(self.usd)
        self.volume_linear_regression = calculate_linear_regression(self.volume)

        self.maximum_loss = 1 - self.lowest_price / self.highest_price
        if self.usd.data[0] != 0:
            self.gain_over_total_listing_period = self.usd.data[len(self.usd.data) - 1] / self.usd.data[0]
        else:
            self.gain_over_total_listing_period = None

    def print(self):
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

        timestamp, usd, btc, volume, market_cap = zip(*csv_input)
        timestamp = list(map(int, timestamp))

        if self.date_limit is not None:
            while timestamp[0] < self.date_limit:
                timestamp = timestamp[1:]
                usd = usd[1:]
                volume = volume[1:]
                btc = btc[1:]
                market_cap = market_cap[1:]

        self.usd = TimeSeries(list(zip(timestamp, usd)))
        self.btc = TimeSeries(list(zip(timestamp, btc)))
        self.volume = TimeSeries(list(zip(timestamp, volume)))
        self.market_cap = TimeSeries(list(zip(timestamp, market_cap)))

        self.data = pandas.DataFrame.from_records(csv_input, columns=header, index=timestamp)
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
        self.print_with_regression(self.usd.data, self.price_linear_regression)

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
        self.print_with_regression(self.volume.data, self.volume_linear_regression)

    def get_financial_data(self):
        return self.usd.data

    def get_volume_financial_data(self):
        return self.volume

    # def calculate_linear_regression_on_volatility(self):
    #     y_values = self.volatility["30"]
    #     return self.calculate_linear_regresseion(y_values)

    # def calculate_linear_regresseion(self, data: pandas.DataFrame):
    #     y_values = list(data[data.columns[0]])
    #     while numpy.isnan(y_values[0]):
    #         y_values.pop(0)
    #     x_values = range(0, len(y_values))
    #
    #     return stats.linregress(x_values, y_values)

    def print_volume_return_correlations(self):
        for correlation in self.volume_return_correlations:
            print(correlation)

    # def calculate_start_date(self):
    #     return self.usd.get_first_timestamp()
    #
    # def get_beginning_date(self):
    #     return self.start_date
#