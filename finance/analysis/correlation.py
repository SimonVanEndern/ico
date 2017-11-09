import csv
import logging
import math
import os.path
from datetime import datetime

import matplotlib.pyplot as plt

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

import numpy

from common.currency_handler import CurrencyHandler


class Correlation:
    currency_handler = CurrencyHandler.Instance()

    def __init__(self):
        return

    def get_return_correlation_data(self, currency0, currency1, date_limit=None):
        return_data_currency0 = self.currency_handler.get_currency(currency0,
                                                                   date_limit=date_limit).calculate_daily_return(
            with_timestamp=True)
        return_data_currency1 = self.currency_handler.get_currency(currency1,
                                                                   date_limit=date_limit).calculate_daily_return(
            with_timestamp=True)

        diff = len(return_data_currency1) - len(return_data_currency0)
        for i in range(int(math.fabs(diff))):
            if diff > 0:
                return_data_currency1.pop(0)
            else:
                return_data_currency0.pop(0)

        _, currency0 = zip(*return_data_currency0)
        _, currency1 = zip(*return_data_currency1)

        correlation = numpy.corrcoef(currency0, currency1)
        return correlation[0][1]

    def get_all_correlations(self, currency, size_limit=100, date_limit=None):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=size_limit)
        output = []

        for other_currency in currencies:
            logger.info("Calculating correlation with " + str(other_currency))
            output.append(
                (other_currency, self.get_return_correlation_data(currency, other_currency, date_limit=date_limit)))

        _, correlations = zip(*output)
        return correlations

    def export_correlation_matrix(self, size_limit=math.inf):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=size_limit)
        output = [currencies]

        for currency in currencies:
            output.append(self.get_all_correlations(currency, size_limit=size_limit))

        output = zip(*output)

        path = os.path.join(os.path.dirname(__file__) + "\\aggregated",
                            "correlation-matrix-" + str(datetime.now().timestamp()) + ".csv")
        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            currencies.insert(0, "")
            writer.writerow(currencies)
            currencies.pop(0)
            for row in output:
                writer.writerow(row)

    def find_highest_correlation(self):
        currencies = []
        correlations = []
        with open(
                "Z:/Google Drive/05 - Projekte/bachelor-thesis/finance/analysis/aggregated/correlation-matrix-1507119023.466763.csv",
                "r") as file:
            reader = csv.reader(file)
            for index, row in enumerate(reader):
                if index == 0:
                    currencies = row
                    continue

                for index2, element in enumerate(row):
                    if index2 == 0:
                        continue
                    correlations.append((currencies[index], currencies[index2], float(element)))

            sorted_correlations = sorted(correlations, key=lambda x: x[2], reverse=True)
            while sorted_correlations[0][2] == 1.0:
                sorted_correlations.pop(0)


run_script = Correlation()
# run_script.export_correlation_matrix()
val1 = run_script.get_all_correlations("bitcoin", size_limit=100)
val1 = list(map(math.fabs, val1))
val2 = run_script.get_all_correlations("bitcoin", date_limit="01.01.2016", size_limit=100)
val2 = list(map(math.fabs, val2))
val3 = run_script.get_all_correlations("bitcoin", date_limit="01.01.2017", size_limit=100)
val3 = list(map(math.fabs, val3))

print(sum(val1))
print(sum(val2))
print(sum(val3))

plt.plot(val1)
plt.plot(val2)
plt.plot(val3)
plt.show()
