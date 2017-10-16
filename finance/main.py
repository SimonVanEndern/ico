from finance.raw_data.raw_data_importer import RawDataImporter
from finance.aggregate_compressed_data.aggregate_compressed_data import ReduceSimplifiedData
from finance.compressed_raw_data.compress_raw_data import SimplifyRawData
from global_data import GlobalData


class MainDataImporter:
    def __init__(self):
        self.raw_data_downloader = RawDataImporter()
        self.raw_data_simplifier = SimplifyRawData()
        self.raw_data_converter = ReduceSimplifiedData()

        self.last_time = GlobalData.last_date_for_download

    def start(self):
        self.raw_data_downloader.download_all_data()
        self.raw_data_simplifier.compress_data(self.last_time)
        self.raw_data_converter.aggregate_compressed_data()
