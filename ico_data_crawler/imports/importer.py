from datetime import datetime

import os

from global_data import GlobalData


class Importer:

    def __init__(self):
        self.path = None

        if GlobalData.ico_use_static_date:
            self.now = datetime.strptime(GlobalData.ico_static_date, "%d.%m.%Y")
        else:
            self.now = datetime.now()

    def get_filename_date(self):
        return str(self.now.year) + str(self.now.month) + str(self.now.day)
    # def construct_path(self):
    #     self.path = os.path.join(os.path.dirname(__file__) + "\saved",
    #                              "blockstarter" + str(self.now.year) + str(self.now.month) + str(self.now.day) + ".html")
