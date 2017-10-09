import csv

import requests
import os.path
from datetime import datetime
import ast


class BitfinexExchangeSource:

    url = "https://api.bitfinex.com/v1/symbols"

    def __init__(self):

        response = requests.request("GET", self.url)

        now = datetime.now()
        path = os.path.join(os.path.dirname(__file__) + "\saved",
                             "bitfinex" + str(now.year) + str(now.month) + str(now.day) + ".csv")

        input = ast.literal_eval(response.text)
        output = set()
        for currency_pair in input:
            first_currency = currency_pair[:3]
            second_currency = currency_pair[3:]

            output.add(first_currency)
            output.add(second_currency)

        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow(["Currency"])
            for symbol in list(output):
                print(symbol)
                writer.writerow([symbol])


run_script = BitfinexExchangeSource()

