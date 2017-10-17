import csv
import json
import logging
import os

from finance.compressed_raw_data.currency_dto import CurrencyDTO
from global_data import GlobalData


class CurrencyCompressor:
    def __init__(self, currency, last_time):
        self.currency = currency
        self.last_time = last_time

        self.raw_data_path = GlobalData.EXTERNAL_PATH_RAW_DATA
        self.additional_data_path = GlobalData.EXTERNAL_PATH_ADDITIONAL_DATA

        self.compressed_only_raw_data_path = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                          GlobalData.FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA)

        self.compressed_with_additional_data_path = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                                 GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA)

        if os.path.isdir(os.path.join(self.raw_data_path, self.currency)):
            if os.path.isfile(os.path.join(self.raw_data_path, self.currency, "ready" + str(last_time))):
                pass
            else:
                logging.info("{}: Currency {} not yet ready for compression".format(self.__class__.__name__, currency))
                return
        else:
            logging.info("{}: Currency {} not yet ready for compression".format(self.__class__.__name__, currency))
            return

        self.compress_data()

    def compress_data(self):
        logging.info("{} Compressing data for {}".format(self.__class__.__name__, self.currency))

        if self.check_if_additional_data_already_compressed():
            logging.info("{}: Currency {} already aggregated with additional data".format(self.__class__.__name__,
                                                                                          self.currency))
            return

        if self.check_if_raw_data_already_compressed():
            logging.info("{}: Currency {} already aggregated".format(self.__class__.__name__, currency))
            return

        currency_dto = self.compress_currency_raw_data()
        if self.check_if_additional_data_available():
            currency_dto = self.compress_additional_data(currency_dto)
            self.save_compressed_data(currency_dto, with_additional_data=True)
        else:
            self.save_compressed_data(currency_dto, with_additional_data=False)

    def check_if_raw_data_already_compressed(self):
        destination_folder = os.path.join(self.compressed_only_raw_data_path, self.currency)
        destination_file = os.path.join(destination_folder, self.currency + self.last_time + ".csv")

        if os.path.isdir(destination_folder):
            if os.path.isfile(destination_file):
                return True

        return False

    def check_if_additional_data_already_compressed(self):
        destination_folder = os.path.join(self.compressed_with_additional_data_path, self.currency)
        destination_file = os.path.join(self.compressed_with_additional_data_path,
                                        self.currency + self.last_time + ".csv")

        if os.path.isdir(destination_folder):
            if os.path.isfile(destination_file):
                return True

        return False

    def check_if_additional_data_available(self):
        destination_folder = os.path.join(self.additional_data_path, self.currency)
        destination_file = os.path.join(self.additional_data_path, "ready" + str(self.last_time))

        if os.path.isdir(destination_folder):
            if os.path.isfile(destination_file):
                return True

        return False

    def compress_currency_raw_data(self):
        currency_dto = CurrencyDTO(self.currency)
        for filename in os.listdir(os.path.join(self.raw_data_path, self.currency)):
            if filename.endswith(".json"):
                with open(os.path.join(self.raw_data_path, self.currency, filename)) as file:
                    raw_data = json.load(file)
                    currency_dto.add_data(raw_data)

        return currency_dto

    def compress_additional_data(self, currency_dto):
        for filename in os.listdir(os.path.join(self.additional_data_path, self.currency)):
            if filename.endswith(".json"):
                with open(os.path.join(self.additional_data_path, self.currency, filename)) as file:
                    raw_data = json.load(file)
                    currency_dto.add_data(raw_data)

        return currency_dto

    def save_compressed_data(self, currency_dto, with_additional_data):
        if with_additional_data:
            filename = os.path.join(self.compressed_with_additional_data_path, self.currency,
                                    self.currency + str(self.last_time) + ".csv")
        else:
            filename = os.path.join(self.compressed_only_raw_data_path, self.currency,
                                    self.currency + str(self.last_time) + ".csv")

        if os.path.isfile(filename):
            raise Exception("File already exists")

        with open(filename, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in currency_dto.to_csv():
                writer.writerow(row)
