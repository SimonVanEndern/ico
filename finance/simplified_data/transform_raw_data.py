import csv
import json
import logging
import os

from common.currency_handler import CurrencyHandler
from finance.simplified_data.currency_dto import CurrencyDTO
from global_data import GlobalData

logging.basicConfig(level=logging.INFO)


class TransformRawData:
    def __init__(self):
        self.source_path = GlobalData.download_raw_data_path_external
        self.destination_path = GlobalData.aggregated_data_path_external
        self.currency_handler = CurrencyHandler()

    def transform_data(self):
        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            self.aggregate_data_into_one_file(currency)

    def aggregate_data_into_one_file(self, currency):
        logging.info("{}: Trying to aggregate Currency {}".format(self.__class__.__name__, currency))

        source_path = os.path.join(self.source_path, currency)
        if not os.path.isdir(source_path) or not os.path.isfile(os.path.join(self.source_path, currency, "ready.txt")):
            logging.info("{}: Currency {} not yet ready for aggregation".format(self.__class__.__name__, currency))
            return

        aggregated_file_filename = os.path.join(self.destination_path, currency + ".csv")

        if os.path.isfile(aggregated_file_filename):
            logging.info("{}: Currency {} already aggregated".format(self.__class__.__name__, currency))
            return

        currency_dto = CurrencyDTO(currency)
        for filename in os.listdir(source_path):
            if filename.endswith(".json"):
                with open(os.path.join(source_path, filename)) as file:
                    raw_data = json.load(file)
                    currency_dto.add_data(raw_data)

        with open(aggregated_file_filename, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in currency_dto.to_csv():
                writer.writerow(row)


TransformRawData().transform_data()
