from os import path

import requests


class Parser:
    import_address = ""
    path_to_save = ""

    def __init__(self):
        self.data = {}
        if path.isfile(self.path_to_save):
            return
        else:
            request = requests.get(self.import_address)
            with open(self.path_to_save, "w") as file:
                file.write(request.text)
