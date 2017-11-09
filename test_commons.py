import os

import sys

from global_data import GlobalData


def save_or_compare_data(data, path):
    if not os.path.isfile(path):
        with open(path, "w") as file:
            file.write(str(data))

    with open(path) as file:
        expected = file.read()
        return expected


class TestCommons:
    def __init__(self):
        # GlobalData.last_date_for_download = GlobalData.TEST_LAST_DATE_FOR_DOWNLOAD
        pass

    def get_test_path(self):
        print(os.path.join(os.path.dirname(sys.modules[self.__class__.__module__].__file__), "test_records",
                           sys._getframe().f_back.f_code.co_name + ".txt"))
        return os.path.join(os.path.dirname(sys.modules[self.__class__.__module__].__file__), "test_records",
                            sys._getframe().f_back.f_code.co_name + ".txt")
