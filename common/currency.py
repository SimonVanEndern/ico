import csv
import datetime
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


# Returns a named tuple with the correlation and p-value
def calculate_correlation(data1, data2):
    return scipy.stats.pearsonr(data1, data2)


class Currency:
    data_path = GlobalData.financial_data

    def __init__(self, currency, data_path=None, date_limit=None):
        self.date_limit = date_limit
        if self.date_limit is not None:
            self.date_limit = datetime.datetime.strptime(date_limit, "%d.%m.%Y")

        if data_path is not None:
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

    def limit_data(self):
        if self.date_limit is None:
            return
        self.data.pop(0)

        while int(self.data[0][0]) < self.date_limit.timestamp() * 1000:
            self.data.pop(0)

    def instantiate(self):

        self.data = self.load_data()
        self.limit_data()
        self.timestamp, self.usd, self.btc, self.volume, self.market_cap = zip(*self.data)

        self.usd = list(self.usd)
        self.usd.pop(0)
        self.usd = list(map(float, self.usd))

        self.volume = list(self.volume)
        self.volume.pop(0)
        self.volume = list(map(float, self.volume))

        self.timestamp = list(self.timestamp)
        self.timestamp.pop(0)
        self.timestamp = list(map(int, self.timestamp))

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

    def get_financial_data(self):
        return list(zip(self.timestamp, self.usd))

    def get_volume_financial_data(self):
        return list(zip(self.timestamp, self.volume))

    def calculate_daily_return(self, with_timestamp=False):
        last = self.usd[0]
        output = []
        for index, price in enumerate(self.usd):
            relative_change = price / last - 1
            if with_timestamp:
                output.append((self.timestamp[index], relative_change))
            else:
                output.append(relative_change)

            last = price
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


run_script = Currency("bitcoin", date_limit="01.11.2016")
run_script.print_course()
run_script.print_volume()
print(run_script.return_volume_correlation)
