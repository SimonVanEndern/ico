import csv
import datetime
import logging
from os import path

import matplotlib.pyplot as plt
import numpy
import pandas
import scipy
from scipy import stats

from common.calculations import calculate_linear_regression, calculate_correlation
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
        self.volatility = None
        self.price_linear_regression = None
        self.volume_linear_regression = None
        self.volume_return_correlations = None
        self.volume_relative_change = None

        self.highest_market_capitalization = None
        self.volume_average = None
        self.total_volume = 0
        self.first_price = 0
        self.highest_price = 0
        self.lowest_price = 0
        self.maximum_loss = 0
        self.gain_over_total_listing_period = 0

        self.instantiate()

        # self.validate_data()

    # def limit_data(self):
    #     if self.date_limit is None:
    #         return
    #     self.financial_data.pop(0)
    #
    #     while int(self.financial_data[0][0]) < self.date_limit.timestamp() * 1000:
    #         self.financial_data.pop(0)

    def instantiate(self):
        # self.limit_data()
        self.logger.info("Initiating currency {}".format(self.currency))

        # self.start_date = self.calculate_start_date()

        # self.volatility = self.calculate_rolling_volatility()
        self.price_linear_regression = calculate_linear_regression(self.usd)
        self.volume_linear_regression = calculate_linear_regression(self.volume)

        # self.volume_return_correlations = self.calculate_volume_return_correlations()

        self.highest_market_capitalization = self.calculate_highest_market_capitalization()
        self.volume_average = self.calculate_volume_average()
        self.total_volume = self.calculate_total_volume()
        self.highest_price = self.calculate_highest_price()
        self.lowest_price = self.calculate_lowest_price()
        self.first_price = self.usd.data[0]
        self.maximum_loss = 1 - self.lowest_price / self.highest_price
        if self.usd.data[0] != 0:
            self.gain_over_total_listing_period = self.usd.data[len(self.usd.data) - 1] / self.usd.data[0]
        else:
            self.gain_over_total_listing_period = None

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

        self.usd = TimeSeries(list(zip(timestamp, usd)))
        self.btc = TimeSeries(list(zip(timestamp, btc)))
        self.volume = TimeSeries(list(zip(timestamp, volume)))
        self.market_cap = TimeSeries(list(zip(timestamp, market_cap)))

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

    # def calculate_rolling_volatility(self, window1=30, window2=90, window3=180):
    #     rolling_1 = []
    #     rolling_2 = []
    #     rolling_3 = []
    #     start = 0
    #     end = len(self.daily_return)
    #     while start + window1 < end:
    #         if start + window3 < end:
    #             rolling_3.append(numpy.std(self.daily_return[start: start + window3]))
    #         else:
    #             rolling_3.insert(0, 0)
    #         if start + window2 < end:
    #             rolling_2.append(numpy.std(self.daily_return[start: start + window2]))
    #         else:
    #             rolling_2.insert(0, 0)
    #
    #         rolling_1.append(numpy.std(self.daily_return[start:start + window1]))
    #         start += 1
    #
    #     output = {"30": rolling_1, "90": rolling_2, "180": rolling_3}
    #     return output

    def calculate_linear_regression_on_volatility(self):
        y_values = self.volatility["30"]
        x_values = range(0, len(y_values))

        # slope, intercept, r_value, p_value, std_err = stats.linregress(x_values, y_values)
        result = stats.linregress(x_values, y_values)
        # plt.plot(x_values, y_values, "--")
        # line = [result.slope * i + result.intercept for i in x_values]
        # plt.plot(x_values, line, "b")
        # plt.show()
        return result

    def calculate_volume_return_correlation(self, smoothing=1):
        val1: TimeSeries = self.volume.calculate_relative_change_smoothed(smoothing=smoothing)
        val2: TimeSeries = self.usd.calculate_relative_change_smoothed(smoothing=smoothing)

        return calculate_correlation(val1, val2)

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

    def calculate_average_volume(self):
        return scipy.mean(self.volume.data)

    def calculate_highest_market_capitalization(self):
        return max(self.market_cap.data)

    def calculate_volume_average(self):
        return numpy.mean(self.volume.data)

    def calculate_total_volume(self):
        return sum(self.volume.data)

    def calculate_highest_price(self):
        if max(self.usd.data) == 0:
            print(self.currency)
        return max(self.usd.data)

    def calculate_lowest_price(self):
        return min(self.usd.data)
