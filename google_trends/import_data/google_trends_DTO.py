import csv
import logging
import os

import pandas
import matplotlib.pyplot as plt

from global_data import GlobalData


class GoogleTrendsDTO:
    def __init__(self, currency):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.currency = currency

        self.no_google_trends_data = False

        self.path_6monthly = os.path.join(GlobalData.EXTERNAL_PATH_GOOGLE_TRENDS_DATA,
                                          GlobalData.FOLDER_GOOGLE_TRENDS_6MONTHLY, self.currency)

        self.filename = self.currency + ".csv"
        self.path_saved_aggregated_data = os.path.join(GlobalData.RELATIVE_GOOGLE_TRENDS_DATA_PATH,
                                                       GlobalData.FOLDER_GOOGLE_TRENDS_6MONTHLY,
                                                       self.filename)

        self.relative_change_6monthly: list = self.load_aggregated_data()
        if not self.relative_change_6monthly:
            self.load_6monthly_raw_data()
            if not self.relative_change_6monthly:
                self.logger.warning("No Google Trends data for Currency {}".format(self.currency))
            else:
                self.first_date = self.relative_change_6monthly[0]
                self.last_date = self.relative_change_6monthly[len(self.relative_change_6monthly) - 1]
                self.save_6_monthly_data()

    def load_6monthly_raw_data(self):
        self.logger.info("Loading Google Trends Data for {}".format(self.currency))
        for filename in os.listdir(self.path_6monthly):
            if filename.endswith(".csv"):
                with open(os.path.join(self.path_6monthly, filename)) as file:
                    reader = csv.reader(file, delimiter=",", lineterminator="\n")
                    data = list(reader)
                    for index, row in enumerate(data):
                        date = int(row[0])
                        if index + 1 < len(data):
                            try:
                                relative_change = int(data[index + 1][1]) / int(row[1]) - 1
                            except ZeroDivisionError:
                                relative_change = 0
                            self.relative_change_6monthly.append((date, relative_change))
                        else:
                            break

        self.relative_change_6monthly = sorted(self.relative_change_6monthly)
        if not self.relative_change_6monthly:
            self.no_google_trends_data = True

    def get_last_500_days(self):
        _, relative = zip(*self.relative_change_6monthly)
        return relative[len(relative) - 500:]

    def print_last_500_days(self):
        df = pandas.DataFrame(list(self.get_last_500_days()))
        plt.plot(df)
        plt.show()

    def save_6_monthly_data(self):
        self.logger.info("Saving Aggregated Google Trends Data for {}".format(self.currency))

        with open(self.path_saved_aggregated_data, "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["Date", "RelativeChange"])
            for element in self.relative_change_6monthly:
                writer.writerow([element[0], element[1]])

    def load_aggregated_data(self) -> list:
        try:
            with open(self.path_saved_aggregated_data) as file:
                reader = csv.reader(file, delimiter=",", lineterminator="\n")
                data = list(reader)
                data.pop(0)
                data = list(map(lambda x: (int(x[0]), float(x[1])), data))
                return data
        except FileNotFoundError:
            return list()


GoogleTrendsDTO("bitcoin").print_last_500_days()
