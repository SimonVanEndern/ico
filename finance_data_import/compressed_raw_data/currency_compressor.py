import csv
import json
import logging
import os

from finance_data_import.compressed_raw_data.currency_dto import CurrencyDTO
from global_data import GlobalData


class CurrencyCompressor:
    def __init__(self, currency, last_time):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.currency = currency
        self.last_time = last_time

        self.raw_data_path = GlobalData.EXTERNAL_PATH_RAW_DATA
        self.additional_data_path = GlobalData.EXTERNAL_PATH_ADDITIONAL_DATA

        self.compressed_only_raw_data_folder = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                            GlobalData.FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA,
                                                            self.currency)

        self.compressed_with_additional_data_folder = os.path.join(GlobalData.EXTERNAL_PATH_COMPRESSED_DATA,
                                                                   GlobalData.FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA,
                                                                   self.currency)

        self.make_folders_if_not_existing()

        if os.path.isdir(os.path.join(self.raw_data_path, self.currency)):
            if os.path.isfile(os.path.join(self.raw_data_path, self.currency, "ready" + str(last_time))):
                pass
            else:
                self.logger.info("Currency {} not yet ready for compression".format(currency))
                return
        else:
            self.logger.info("Currency {} not yet ready for compression".format(currency))
            return

        self.compress_data()

    def make_folders_if_not_existing(self):
        if not os.path.isdir(self.compressed_with_additional_data_folder):
            os.mkdir(self.compressed_with_additional_data_folder)

        if not os.path.isdir(self.compressed_only_raw_data_folder):
            os.mkdir(self.compressed_only_raw_data_folder)

    def compress_data(self):
        self.logger.info("Compressing data for {}".format(self.currency))

        if self.check_if_additional_data_already_compressed():
            self.logger.info("Currency {} already compressed with additional data".format(self.currency))
            return

        currency_dto = self.compress_currency_raw_data()
        if self.check_if_additional_data_available():
            currency_dto = self.compress_additional_data(currency_dto)
            self.save_compressed_data(currency_dto, with_additional_data=True)
        else:
            if self.check_if_raw_data_already_compressed():
                self.logger.info("Currency {} already compressed".format(self.currency))
                return
            else:
                self.save_compressed_data(currency_dto, with_additional_data=False)

    def check_if_raw_data_already_compressed(self):
        destination_file = os.path.join(self.compressed_only_raw_data_folder,
                                        self.currency + str(self.last_time) + ".csv")

        return os.path.isfile(destination_file)

    def check_if_additional_data_already_compressed(self):
        destination_file = os.path.join(self.compressed_with_additional_data_folder,
                                        self.currency + str(self.last_time) + ".csv")

        return os.path.isfile(destination_file)

    def check_if_additional_data_available(self):
        destination_folder = os.path.join(self.additional_data_path, self.currency)
        destination_file = os.path.join(destination_folder, "ready" + str(self.last_time))

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
            destination_file = os.path.join(self.compressed_with_additional_data_folder,
                                            self.currency + str(self.last_time) + ".csv")
        else:
            destination_file = os.path.join(self.compressed_only_raw_data_folder,
                                            self.currency + str(self.last_time) + ".csv")

        if os.path.isfile(destination_file):
            raise Exception("File already exists")

        with open(destination_file, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            for row in currency_dto.to_csv():
                writer.writerow(row)
