from datetime import datetime

import os

from global_data import GlobalData


class Importer:

    def __init__(self):
        self.path = None

        if GlobalData.ICO_USE_STATIC_DATE:
            self.now = datetime.strptime(GlobalData.ICO_STATIC_DATE, "%d.%m.%Y")
        else:
            self.now = datetime.now()

    def get_filename_date(self):
        return str(self.now.year) + str(self.now.month) + str(self.now.day)
