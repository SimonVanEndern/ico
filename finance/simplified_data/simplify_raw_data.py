import csv
import json
import logging
import os

from common.currency_handler import CurrencyHandler
from finance.simplified_data.currency_dto import CurrencyDTO
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class SimplifyRawData:
    def __init__(self):
        self.source_path = GlobalData.EXTERNAL_PATH_RAW_DATA
        self.additional_source_path = GlobalData.EXTERNAL_PATH_ADDITIONAL_DATA
        self.destination_path = GlobalData.EXTERNAL_PATH_AGGREGATED_DATA
        self.currency_handler = CurrencyHandler()

    # Main
    def compress_data(self, last_time):
        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            currency_dto = self.aggregate_data_from_all_files(currency)
            if currency_dto is not None:
                self.save_compressed_data_into_one_file(currency_dto.to_csv(), currency)

    def aggregate_data_from_all_files(self, currency, only_save_if_not_yet_saved=True):
        logging.info("{}: Starting to aggregate Currency {}".format(self.__class__.__name__, currency))

        source_path = os.path.join(self.source_path, currency)
        additional_source_path = os.path.join(self.additional_source_path, currency)

        aggregated_file_filename = os.path.join(self.destination_path, currency + ".csv")

        if not os.path.isdir(source_path) or not os.path.isfile(os.path.join(self.source_path, currency, "ready.txt")):
            logging.info("{}: Currency {} not yet ready for aggregation".format(self.__class__.__name__, currency))
            return

        if os.path.isfile(aggregated_file_filename):
            logging.info("{}: Currency {} already aggregated".format(self.__class__.__name__, currency))
            if only_save_if_not_yet_saved:
                return

        currency_dto = CurrencyDTO(currency)
        for filename in os.listdir(source_path):
            if filename.endswith(".json"):
                with open(os.path.join(source_path, filename)) as file:
                    raw_data = json.load(file)
                    currency_dto.add_data(raw_data)

        if os.path.isdir(additional_source_path):
            for filename in os.listdir(additional_source_path):
                if filename.endswith(".json"):
                    with open(os.path.join(additional_source_path, filename)) as file:
                        raw_data = json.load(file)
                        currency_dto.add_data(raw_data)

        return currency_dto

    def save_compressed_data_into_one_file(self, data, currency):
        aggregated_file_filename = os.path.join(self.destination_path, currency + ".csv")

        with open(aggregated_file_filename, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in data:
                writer.writerow(row)


# SimplifyRawData().simplify_data()
