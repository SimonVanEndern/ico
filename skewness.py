import matplotlib.pyplot as plt
import numpy
import pandas

from common.currency_handler import CurrencyHandler


class Skewness:
    cf = CurrencyHandler.Instance()

    def __init__(self, attribute):
        all_currency_names = self.cf.get_all_currency_names()
        all_currencies = list(map(lambda x: self.cf.get_currency(x), all_currency_names))

        skewness = list()
        log_skewness = list()
        percentage_positive_return = list()

        for currency in all_currencies:
            relative_data_of_attribute = currency.relative_data[attribute]
            relative_data_of_attribute = relative_data_of_attribute[numpy.isfinite(relative_data_of_attribute)]
            relative_data_of_attribute = relative_data_of_attribute.dropna()

            log_relative_data_of_attribute = currency.log_relative_data[attribute]
            log_relative_data_of_attribute = log_relative_data_of_attribute[
                numpy.isfinite((log_relative_data_of_attribute))]
            log_relative_data_of_attribute = log_relative_data_of_attribute.dropna()

            skewness.append(relative_data_of_attribute.skew())
            log_skewness.append(log_relative_data_of_attribute.skew())
            percentage_positive_return.append(sum(relative_data_of_attribute > 0) / len(relative_data_of_attribute))

        print("Skewness on returns")
        print(pandas.Series(skewness).describe())
        print("Percentage of positive returns")
        print(pandas.Series(percentage_positive_return).describe())
        pandas.Series(skewness).hist(bins=50)
        plt.show()
        pandas.Series(percentage_positive_return).hist(bins=50)
        plt.show()

        print("Log Skewness on returns")
        print(pandas.Series(log_skewness).describe())
        pandas.Series(log_skewness).hist(bins=50)
        plt.show()


Skewness("usd")
Skewness("volume")
