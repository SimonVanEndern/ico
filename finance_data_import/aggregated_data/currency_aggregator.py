import csv
import logging
import os
from typing import List

from finance_data_import.aggregated_data import financial_data_calculator
from finance_data_import.aggregated_data.financial_data_calculator import FinancialDataCalculator
from finance_data_import.dto import DTO
from global_data import GlobalData


class CurrencyAggregator(DTO):
    def __init__(self, currency: str, last_time: int, interval: int):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.success: bool = False
        self.currency: str = currency
        self.last_time: int = last_time
        self.header = None
        self.interval = interval

        self.fdc: FinancialDataCalculator = FinancialDataCalculator()

        self.compressed_only_raw_data_folder: str = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                                 GlobalData.FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA,
                                                                 self.currency)

        self.compressed_with_additional_data_folder: str = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                                        GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA,
                                                                        self.currency)

        self.aggregated_with_additional_data_folder: str = os.path.join(GlobalData.EXTERNAL_PATH_AGGREGATED_DATA,
                                                                        GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA,
                                                                        self.currency)

        self.output_filename: str = self.currency + "-" + str(self.interval) + "hourly-" + str(self.last_time) + ".csv"
        self.input_filename: str = self.currency + str(self.last_time) + ".csv"

        super().__init__(self.aggregated_with_additional_data_folder, self.output_filename)

    def run(self):
        if os.path.isdir(self.aggregated_with_additional_data_folder):
            if os.path.isfile(os.path.join(self.aggregated_with_additional_data_folder, self.output_filename)):
                self.logger.info("Currency {} already aggregated".format(self.currency))
                return
        else:
            os.mkdir(self.aggregated_with_additional_data_folder)

        aggregated_data: List[list] = self.aggregate_currency()
        if len(aggregated_data) > 0:
            super().save_to_csv(aggregated_data)
            super().set_success(True)

    def aggregate_currency(self) -> List[list]:
        input_file = os.path.join(self.compressed_with_additional_data_folder, self.input_filename)
        if not os.path.isfile(input_file):
            input_file = os.path.join(self.compressed_only_raw_data_folder, self.input_filename)
        if not os.path.isfile(input_file):
            self.logger.info("Currency {} not yet ready for aggregation".format(self.currency))
            return list()

        self.logger.info("Aggregating Currency {}".format(self.currency))

        raw_data = self.get_compressed_data(input_file)
        aggregated_data = self.aggregate_data(raw_data, self.interval)
        return aggregated_data

    def get_compressed_data(self, input_file: str) -> List:
        with open(input_file) as file:
            reader = csv.reader(file)
            compressed_raw_data = list(reader)
            super().set_header(compressed_raw_data.pop(0))
            return compressed_raw_data

    def aggregate_data(self, data, step_in_hours: int) -> List[list]:
        data = list(map(lambda x: {"time": int(x[0]), "data": list(map(float, x[1:]))}, data))
        start: int = financial_data_calculator.get_next_timestamp_at_time(int(data[0]["time"]), 12)
        end: int = financial_data_calculator.get_last_timestamp_at_time(int(data[len(data) - 1]["time"]), 12)
        step: int = 1000 * 3600 * step_in_hours
        reduced_data = self.fdc.calculate_series_for_timestamp(start, end, step, data, self.currency,
                                                               maximum_time_span=step_in_hours)
        reduced_data = list(map(lambda x: [x['time']] + x['data'], reduced_data))
        return reduced_data
