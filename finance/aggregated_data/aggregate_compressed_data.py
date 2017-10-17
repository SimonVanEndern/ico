import csv
import logging
import os

from common.currency_handler import CurrencyHandler
from finance.aggregated_data import financial_data_calculator
from finance.aggregated_data.financial_data_calculator import FinancialDataCalculator
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class ReduceSimplifiedData:
    def __init__(self):
        self.currency_handler = CurrencyHandler()
        self.source_path = GlobalData.EXTERNAL_PATH_AGGREGATED_DATA
        self.destination_path = GlobalData.EXTERNAL_PATH_COMPRESSED_DATA
        self.header = None
        self.fdc = FinancialDataCalculator()

        self.last_timestamp = GlobalData.last_date_for_download

    def aggregate_compressed_data(self):
        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            if not os.path.isfile(os.path.join(self.source_path, currency + ".csv")):
                logging.info("{}: Currency {} not yet ready for reduction".format(self.__class__.__name__, currency))
                continue

            if os.path.isfile(os.path.join(self.destination_path, currency + ".csv")):
                logging.info("{}: Currency {} already reduced".format(self.__class__.__name__, currency))
                continue

            logging.info("{}: Reducing Currency {}".format(self.__class__.__name__, currency))

            raw_data = self.get_raw_data(currency)
            reduced_data = self.aggregate_data(raw_data, currency)
            self.export_aggregated_data(currency, reduced_data)

        if os.path.isfile(
                os.path.join(GlobalData.EXTERNAL_PATH_RAW_DATA, "ready-" + str(self.last_timestamp))):
            open(os.path.join(GlobalData.EXTERNAL_PATH_AGGREGATED_DATA, "ready-" + str(self.last_timestamp))).close()
            logging.info(
                "{}: All currencies until {} already downloaded".format(self.__class__.__name__, self.last_timestamp))

    def get_raw_data(self, currency):
        with open(os.path.join(self.source_path, currency + ".csv")) as file:
            reader = csv.reader(file)
            raw_data = list(reader)
            self.header = raw_data.pop(0)
            return raw_data

    def aggregate_data(self, data, currency):
        data = list(map(lambda x: {"time": int(x[0]), "data": list(map(float, x[1:]))}, data))
        start = financial_data_calculator.get_next_timestamp_at_time(int(data[0]["time"]), 12)
        end = financial_data_calculator.get_last_timestamp_at_time(int(data[len(data) - 1]["time"]), 12)
        step = 1000 * 3600 * 24
        reduced_data = self.fdc.calculate_series_for_timestamp(start, end, step, data, currency)
        reduced_data = list(map(lambda x: [x['time']] + x['data'], reduced_data))
        return reduced_data

    def export_aggregated_data(self, currency, data):
        with open(os.path.join(self.destination_path, currency + ".csv"), "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(self.header)
            for row in data:
                writer.writerow(row)


ReduceSimplifiedData().aggregate_compressed_data()
