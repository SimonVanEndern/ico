import csv
import math
import os.path
from datetime import datetime

import numpy

from common.currency import Currency


class Correlation:
    # Change away from static bitcoin
    currency = Currency("bitcoin")

    def __init__(self):
        return

    def get_return_correlation_data(self, currency0, currency1):
        return_data_currency0 = self.currency.get_return_data(currency0)
        return_data_currency1 = self.currency.get_return_data(currency1)

        diff = len(return_data_currency1) - len(return_data_currency0)
        for i in range(int(math.fabs(diff))):
            if diff > 0:
                return_data_currency1.pop(0)
            else:
                return_data_currency0.pop(0)

        _, currency0 = zip(*return_data_currency0)
        _, currency1 = zip(*return_data_currency1)

        combined = list(zip(_, currency0, currency1))

        # plt.plot(_, currency0)
        # plt.plot(_, currency1)
        # plt.show()

        correlation = numpy.corrcoef(currency0, currency1)
        # print(correlation[0][1])
        return correlation[0][1]

    def get_all_correlations(self, currency, size_limit=100):
        currencies = self.currency.get_currencies_from_file_names(size_limit=size_limit)
        output = []

        for other_currency in currencies:
            output.append((other_currency, self.get_return_correlation_data(currency, other_currency)))

        # print(output)
        _, correlations = zip(*output)
        # correlations = map(math.fabs, correlations)
        print(sorted(correlations, reverse=True))
        return correlations

    def export_correlation_matrix(self, size_limit=math.inf):
        currencies = self.currency.get_currencies_from_file_names(size_limit=size_limit)
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
                # if index == 700:
                #     break

                for index2, element in enumerate(row):
                    if index2 == 0:
                        continue
                    correlations.append((currencies[index], currencies[index2], float(element)))

            print(correlations)
            print(len(correlations))
            sorted_correlations = sorted(correlations, key=lambda x: x[2], reverse=True)
            while sorted_correlations[0][2] == 1.0:
                sorted_correlations.pop(0)

            print(sorted_correlations[:200])


run_script = Correlation()
# run_script.export_correlation_matrix()
run_script.find_highest_correlation()
