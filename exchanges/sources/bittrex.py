import csv

import requests
import os.path
from datetime import datetime
import ast
import json


class BittrexExchangeSource:

    url = "https://bittrex.com/api/v1.1/public/getcurrencies"

    def __init__(self):

        response = requests.request("GET", self.url)

        now = datetime.now()
        path = os.path.join(os.path.dirname(__file__) + "\saved",
                             "bittrex" + str(now.year) + str(now.month) + str(now.day) + ".csv")

        input = json.loads(response.text)
        output = []
        for currency in input["result"]:
            output.append(currency["Currency"])

        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow(["Currency"])
            for symbol in list(output):
                print(symbol)
                writer.writerow([symbol])


run_script = BittrexExchangeSource()

