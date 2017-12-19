import logging

from finance_data_import.aggregated_data.aggregate_compressed_data import ReduceSimplifiedData
from finance_data_import.compressed_raw_data.compress_raw_data import SimplifyRawData
from finance_data_import.raw_data.raw_data_importer import RawDataImporter
from global_data import GlobalData


class MainDataImporter:
    # logging.basicConfig(level=logging.INFO, input_filename="logging.log")
    logging.basicConfig(level=logging.INFO)

    def __init__(self):
        self.raw_data_downloader = RawDataImporter()
        self.raw_data_simplifier = SimplifyRawData()
        self.raw_data_converter = ReduceSimplifiedData()

        self.last_time = GlobalData.LAST_DATA_FOR_DOWNLOAD
        self.interval = 24  # hours

    def run(self):
        self.raw_data_downloader.download_all_data()
        self.raw_data_simplifier.compress_data(self.last_time)
        self.raw_data_converter.aggregate_compressed_data(self.last_time, self.interval)


MainDataImporter().run()
