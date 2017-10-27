import csv
import logging
import os
import time
from datetime import datetime

from pytrends.request import TrendReq

from common.currency_handler import CurrencyHandler
from global_data import GlobalData
from google_trends.import_data.google_trends_DTO import GoogleTrendsDTO

logging.basicConfig(level=logging.INFO)


class GoogleTrends:
    def __init__(self):
        self.trend_api = TrendReq()
        self.save_path = GlobalData.EXTERNAL_PATH_GOOGLE_TRENDS_DATA
        self.save_path = os.path.join(self.save_path, "6monthly")
        self.start_2013 = 1356998400000
        self.end = 1508157562847

        self.currency_handler = CurrencyHandler()

    def main(self):
        self.import_data()
        self.aggregate_data()

    def aggregate_data(self):
        for currency in self.currency_handler.get_all_currency_names():
            GoogleTrendsDTO(currency)

    def import_data(self):
        for currency in self.currency_handler.get_all_currency_names():
            logging.info("{}:Start download Google Trends data for {}".format(self.__class__.__name__, currency))
            start = self.start_2013
            step = 180 * 24 * 3600 * 1000
            while start + step < self.end:
                start_date = datetime.fromtimestamp(start / 1e3).strftime("%Y-%m-%d")
                end_date = datetime.fromtimestamp((start + step) / 1e3).strftime("%Y-%m-%d")
                start += step

                self.get_or_download(currency, start_date, end_date)

    def get_or_download(self, currency, start, end):
        path = os.path.join(self.save_path, currency)

        if not os.path.isdir(path):
            os.mkdir(path)

        filename = currency + str(start) + "-" + str(end) + ".csv"

        if os.path.isfile(os.path.join(path, filename)):
            logging.info("{}:Google Trends data for {} already downloaded".format(self.__class__.__name__, currency))
            return
        else:
            raw_data = self.get_raw_data(currency, start + " " + end)
            compressed_data = self.compress_raw_data(raw_data)
            self.save_compressed_data(compressed_data, path, filename)

    def get_raw_data(self, search_term, time_frame):
        time.sleep(2)
        self.trend_api.build_payload([search_term], timeframe=time_frame)
        return self.trend_api.interest_over_time()

    def compress_raw_data(self, raw_data):
        output = []
        for entry in raw_data:
            output.append({'time': int(entry['time']), 'value': entry['value'][0]})

        return output

    def save_compressed_data(self, data, save_path, filename):
        with open(os.path.join(save_path, filename), "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            for row in data:
                writer.writerow([row['time'], row['value']])


GoogleTrends().main()
# data = trends.get_raw_data("bitcoin", "2017-04-16 2017-10-16")
# print(trends.compress_raw_data(data))
