from finance.raw_data.raw_data_importer import RawDataImporter
from finance.reduced_simplified_data.reduce_raw_data import ReduceSimplifiedData
from finance.simplified_data.simplify_raw_data import SimplifyRawData


class MainDataImporter:
    def __init__(self):
        self.raw_data_downloader = RawDataImporter()
        self.raw_data_simplifier = SimplifyRawData()
        self.raw_data_converter = ReduceSimplifiedData()

    def start(self):
        self.raw_data_downloader.download_all_data()
        self.raw_data_simplifier.simplify_data()
        self.raw_data_converter.reduce_simplified_data()
