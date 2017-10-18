import csv
import logging
import os

from finance.aggregated_data import financial_data_calculator
from finance.aggregated_data.financial_data_calculator import FinancialDataCalculator
from finance.dto import DTO
from global_data import GlobalData


class CurrencyAggregator(DTO):
    def __init__(self, currency, last_time):
        self.success = False
        self.currency = currency
        self.last_time = last_time
        self.header = None

        self.fdc = FinancialDataCalculator()

        self.compressed_only_raw_data_folder = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                            GlobalData.FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA,
                                                            self.currency)

        self.compressed_with_additional_data_folder = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                                   GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA,
                                                                   self.currency)

        self.aggregated_with_additional_data_folder = os.path.join(GlobalData.EXTERNAL_PATH_AGGREGATED_DATA,
                                                                   GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA,
                                                                   self.currency)

        self.filename = self.currency + str(self.last_time) + ".csv"

        super().__init__(self.aggregated_with_additional_data_folder, self.filename)

        # self.run()

    def run(self):
        if os.path.isdir(self.aggregated_with_additional_data_folder):
            if os.path.isfile(os.path.join(self.aggregated_with_additional_data_folder, self.filename)):
                logging.info("{}: Currency {} already aggregated".format(self.__class__.__name__, self.currency))
                return
        else:
            os.mkdir(self.aggregated_with_additional_data_folder)

        aggregated_data = self.aggregate_currency()
        super().save_to_csv(aggregated_data)
        super().set_success(True)

    def aggregate_currency(self):
        input_file = os.path.join(self.compressed_with_additional_data_folder, self.filename)
        if not os.path.isfile(input_file):
            input_file = os.path.join(self.compressed_only_raw_data_folder, self.filename)
        if not os.path.isfile(input_file):
            logging.info("{}: Currency {} not yet ready for aggregation".format(self.__class__.__name__, self.currency))
            return

        logging.info("{}: Aggregating Currency {}".format(self.__class__.__name__, self.currency))

        if self.currency == "parallelcoin":
            pass

        raw_data = self.get_compressed_data(input_file)
        aggregated_data = self.aggregate_data(raw_data)
        return aggregated_data

    def get_compressed_data(self, input_file):
        with open(input_file) as file:
            reader = csv.reader(file)
            raw_data = list(reader)
            super().set_header(raw_data.pop(0))
            return raw_data

    def aggregate_data(self, data):
        data = list(map(lambda x: {"time": int(x[0]), "data": list(map(float, x[1:]))}, data))
        start = financial_data_calculator.get_next_timestamp_at_time(int(data[0]["time"]), 12)
        end = financial_data_calculator.get_last_timestamp_at_time(int(data[len(data) - 1]["time"]), 12)
        step = 1000 * 3600 * 24
        reduced_data = self.fdc.calculate_series_for_timestamp(start, end, step, data, self.currency)
        reduced_data = list(map(lambda x: [x['time']] + x['data'], reduced_data))
        return reduced_data
