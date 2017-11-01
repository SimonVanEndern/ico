import csv
import datetime
import logging
from os import path

import matplotlib.pyplot as plt
import numpy
import pandas
from scipy import stats

from common.calculations import calculate_linear_regression
from common.time_series import TimeSeries
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class Currency:
    data_path = GlobalData.financial_data_path

    def __init__(self, currency, data_path=None, date_limit=None):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.date_limit = date_limit
        if self.date_limit is not None:
            self.date_limit = datetime.datetime.strptime(date_limit, "%d.%m.%Y")
            self.date_limit = int(self.date_limit.timestamp() * 1e3)

        if data_path is not None:
            self.data_path: str = data_path

        self.currency: str = currency
        self.logger.info("Initiating currency {}".format(self.currency))

        # Inputs
        self.usd: TimeSeries = None
        self.btc: TimeSeries = None
        self.market_cap: TimeSeries = None
        self.volume: TimeSeries = None

        self.load_financial_data()

        # Augmentations
        self.start_date: int = self.calculate_start_date()

        # Calculations
        self.daily_return: int = None
        self.volatility = dict()
        self.price_linear_regression = None
        self.volume_linear_regression = None
        self.volume_return_correlations = None
        self.volume_relative_change = None

        self.volume_average = None
        self.total_volume = 0
        self.first_price = 0
        self.highest_price = 0
        self.lowest_price = 0
        self.maximum_loss = 0
        self.gain_over_total_listing_period = 0

        self.data: pandas.DataFrame = None

        self.instantiate()

    def instantiate(self):
        # self.limit_data()
        self.logger.info("Initiating currency {}".format(self.currency))

        self.price_linear_regression = calculate_linear_regression(self.usd)
        self.volume_linear_regression = calculate_linear_regression(self.volume)

        self.volume_return_corrs = self.calculate_volume_return_correlation()

        self.highest_market_capitalization = self.calculate_highest_market_capitalization()
        self.maximum_loss = 1 - self.lowest_price / self.highest_price
        if self.usd.data[0] != 0:
            self.gain_over_total_listing_period = self.usd.data[len(self.usd.data) - 1] / self.usd.data[0]
        else:
            self.gain_over_total_listing_period = None

        self.daily_return = self.calculate_daily_return()
        self.volatility = self.calculate_rolling_volatility()

    def print(self):
        print("Currency: {} - Gaps: {}".format(self.currency, self.usd.number_of_gaps()))
        print("Volume return correlation: {}".format(self.volume_return_corrs))

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

    def calculate_rolling_volatility(self, windows=None) -> dict:
        if windows is None:
            windows = [30, 90, 180]

        output: dict = dict()
        for window in windows:
            output[str(window)] = pandas.rolling_std(self.usd.relative_change, window)

        return output

    def calculate_linear_regression_on_volatility(self):
        y_values = self.volatility["30"]
        return self.calculate_linear_regresseion(y_values)

    def calculate_linear_regresseion(self, data: pandas.DataFrame):
        y_values = list(data[data.columns[0]])
        while numpy.isnan(y_values[0]):
            y_values.pop(0)
        x_values = range(0, len(y_values))

        return stats.linregress(x_values, y_values)

    def calculate_volume_return_correlation(self, smoothing=1):
        val1_pandas: pandas.DataFrame = self.volume.calculate_relative_change_smoothed(smoothing)
        val2_pandas: pandas.DataFrame = self.usd.calculate_relative_change_smoothed(smoothing)

        joint_df = val1_pandas.join(val2_pandas, lsuffix="first")

        return joint_df.corr(method="pearson")[joint_df.columns[0]][1]

    def calculate_volume_return_correlations(self):
        output = []
        for i in [1, 2, 3, 5, 7, 11, 17, 19, 23, 27, 29, 31, 37, 41, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 91]:
            output.append(self.calculate_volume_return_correlation(smoothing=i))

        return output

    def print_volume_return_correlations(self):
        for correlation in self.volume_return_correlations:
            print(correlation)

    def calculate_start_date(self):
        return self.usd.get_first_timestamp()

    def get_beginning_date(self):
        return self.start_date

    def calculate_highest_market_capitalization(self):
        return max(self.market_cap.data)

    def calculate_daily_return(self):
        return self.usd.relative_change
