import csv
import math
import os.path
from os import path

import matplotlib.pyplot as plt
import numpy
import pandas
import scipy
from scipy import stats

from globals import GlobalData


def calculate_linear_regression(usd):
    return stats.linregress(range(0, len(usd)), usd)


def calculate_relative_change(data):
    last = data[0]
    output = []
    for course in data:
        if last == 0:
            output.append(0)
        else:
            # In case that volume at the last day was zero
            output.append(course / last - 1)
        last = course

    return output


def calculate_correlation(data1, data2):
    print(numpy.corrcoef(data1, data2)[0][1])
    return scipy.stats.pearsonr(data1, data2)


class Currency:
    data_path = GlobalData.financial_data

    def __init__(self, extended=False, currency="", data_path=""):
        if extended:
            if data_path != "":
                self.data_path = data_path

            self.name = currency

            # Inputs
            self.data = None
            self.timestamp = None
            self.usd = None
            self.btc = None
            self.market_cap = None
            self.volume = None

            # Calculations
            self.daily_return = None
            self.volatility = None
            self.price_linear_regression = None
            self.volume_linear_regression = None
            self.return_volume_correlation = None
            self.volume_relative_change = None

            self.instantiate()

    def instantiate(self):
        self.data = self.load_data()
        self.timestamp, self.usd, self.btc, self.volume, self.market_cap = zip(*self.data)

        self.usd = list(self.usd)
        self.usd.pop(0)
        self.usd = list(map(float, self.usd))

        self.volume = list(self.volume)
        self.volume.pop(0)
        self.volume = list(map(float, self.volume))

        self.daily_return = self.calculate_daily_return()
        self.volatility = self.calculate_rolling_volatility()
        self.price_linear_regression = calculate_linear_regression(self.usd)
        self.volume_linear_regression = calculate_linear_regression(self.volume)

        self.volume_relative_change = calculate_relative_change(self.volume)
        self.return_volume_correlation = calculate_correlation(self.volume_relative_change, self.daily_return)

    def load_data(self):
        with open(path.join(self.data_path, self.name + ".csv"), "r") as file:
            reader = csv.reader(file)
            return list(reader)

    @staticmethod
    def print_with_regression(data, regression):
        df = pandas.DataFrame(data)
        x_values = range(0, len(data))
        y_values = [regression.slope * i + regression.intercept for i in x_values]
        plt.plot(x_values, y_values, "--")
        plt.plot(df)
        plt.show()

    def print_course(self):
        self.print_with_regression(self.usd, self.price_linear_regression)

    def print_daily_return(self):
        df = pandas.DataFrame(self.daily_return)
        df2 = pandas.DataFrame(self.volume_relative_change)
        plt.plot(df2)
        plt.plot(df)
        plt.show()

    def print_volatility(self):
        df = pandas.DataFrame.from_dict(self.volatility)
        df.plot()
        plt.show()

    def print_volume(self):
        self.print_with_regression(self.volume, self.volume_linear_regression)

    def get_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            usd = map(float, usd)

            return list(zip(timestamp, usd))

    def get_volume_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            volume = map(int, volume)

            return list(zip(timestamp, volume))

    def get_market_cap_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(file)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            volume = map(int, volume)

            return list(zip(timestamp, ))

    def get_currencies_from_file_names(self, size_limit=math.inf):
        output = []
        for index, filename in enumerate(os.listdir(self.data_path)):
            if index == size_limit:
                return output

            output.append(filename.split(".")[0])

        return output

    def get_return_data(self, currency):
        input = self.get_financial_data(currency)

        output = []
        for index, element in enumerate(input):
            if index == 0:
                continue
            output.append((element[0], (element[1] / input[index - 1][1]) - 1))

        return output

    @staticmethod
    def return_data_to_dict(data):
        output = {}
        for timestamp, datapoint in data:
            output[timestamp] = datapoint

        return output

    def calculate_daily_return(self):
        last = self.usd[0]
        output = []
        for course in self.usd:
            output.append(course / last - 1)
            last = course

        # No removing, because we need same number of datapoints
        # Remove first element which is 0.0
        # output.pop(0)
        return output

    def calculate_rolling_volatility(self, window1=30, window2=90, window3=180):
        rolling_1 = []
        rolling_2 = []
        rolling_3 = []
        start = 0
        end = len(self.daily_return)
        while start + window1 < end:
            if start + window3 < end:
                rolling_3.append(numpy.std(self.daily_return[start: start + window3]))
            else:
                rolling_3.insert(0, 0)
            if start + window2 < end:
                rolling_2.append(numpy.std(self.daily_return[start: start + window2]))
            else:
                rolling_2.insert(0, 0)

            rolling_1.append(numpy.std(self.daily_return[start:start + window1]))
            start += 1

        output = {"30": rolling_1, "90": rolling_2, "180": rolling_3}
        return output

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


run_script = Currency(extended=True, currency="bitcoin")
run_script.print_course()
run_script.print_volume()
# run_script.print_daily_return()
# run_script.calculate_linear_regression_on_volatility()
# run_script.get_return_correlation_data("bitcoin", "ethereum")
# run_script.get_return_correlation_data("bitcoin", "litecoin")
# run_script.get_return_correlation_data("ethereum", "litecoin")
# run_script.get_return_correlation_data("ripple", "litecoin")
# run_script.get_return_correlation_data("ripple", "bitcoin")
# run_script.get_return_correlation_data("ripple", "ethereum")
# run_script.get_all_correlations()
