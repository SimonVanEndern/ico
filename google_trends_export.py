import csv

import numpy
import pandas
import time

from common.currency_handler import CurrencyHandler


class GoogleTrendsExport:

    def __init__(self):
        self.ch = CurrencyHandler.Instance()

        all_currency_names = self.ch.get_all_currency_names()
        all_currencies = list(map(lambda x: self.ch.get_currency(x), all_currency_names))

        google_trends = list(map(lambda x: (x.currency, x.google_trends_data.relative_change_6monthly), all_currencies))

        google_trends = list(filter(lambda x: len(x[1]) > 0, google_trends))
        names = list(map(lambda x: x[0], google_trends))
        google_trends = list(map(lambda x: x[1], google_trends))

        frames = list()

        all_indices = list()

        for trend in google_trends:
            index, data = zip(*trend)
            for i in list(index):
                if i not in all_indices:
                    all_indices.append(i)
            frames.append(pandas.DataFrame(list(data), index=index))

        all_indices.sort()
        print(all_indices)

        with open("google-trends-export.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["TIMESTAMP"] + names)
            for index in all_indices:
                print(index)
                row = [index]
                for trend in frames:
                    if index in trend.index:
                        # print(index)
                        # print(trend)
                        # time.sleep(5)
                        row.append(trend[trend.columns[0]][index])
                    else:
                        row.append(numpy.nan)
                writer.writerow(row)


GoogleTrendsExport()
