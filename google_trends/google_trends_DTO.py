import csv
import os

from global_data import GlobalData


class GoogleTrendsDTO:
    def __init__(self, currency):
        self.currency = currency

        self.path_6monthly = os.path.join(GlobalData.EXTERNAL_PATH_GOOGLE_TRENDS_DATA,
                                          GlobalData.FOLDER_GOOGLE_TRENDS_6MONTHLY, self.currency)

        self.relative_change_6monthly = dict()
        self.load_6monthly_data()

    def load_6monthly_data(self):
        for filename in os.listdir(self.path_6monthly):
            if filename.endswith(".csv"):
                with open(os.path.join(self.path_6monthly, filename)) as file:
                    reader = csv.reader(file, delimiter=",", lineterminator="\n")
                    data = list(reader)
                    for index, row in enumerate(data):
                        date = int(row[0])
                        if index + 1 < len(data):
                            relative_change = int(data[index + 1][1]) / int(row[1]) - 1
                            self.relative_change_6monthly[date] = relative_change
                        else:
                            break


GoogleTrendsDTO("bitcoin")
