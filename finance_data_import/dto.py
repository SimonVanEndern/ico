import csv

import os
from typing import List


class DTO:

    def __init__(self, export_folder: str, export_file: str):
        self.export_path: str = os.path.join(export_folder, export_file)
        self.success: bool = False
        self.header: list = None

    def check_success(self):
        return self.success

    def set_success(self, success):
        self.success = success

    def set_header(self, header):
        self.header = header

    def save_to_csv(self, data: List[list]):
        if self.header is None:
            raise Exception("No header present")

        if os.path.isfile(self.export_path):
            raise Exception("File already exists")

        with open(self.export_path, "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(self.header)
            for row in data:
                writer.writerow(row)
