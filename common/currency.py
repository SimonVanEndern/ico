import csv
import os.path

import math

import common.coinmarketCapApi


class Currency:
    data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-09-28"
    example_currency = "bitcoin"
    coinmarketcap = common.coinmarketCapApi.CoinmarketCapApi()

    def __init__(self):
        return

    def get_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            usd = map(float, usd)
            # output = {}
            # for idx, element in enumerate(timestamp):
            #     output[element] = usd[idx]

            return list(zip(timestamp, usd))

    def get_volume_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(reader)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            volume = map(int, volume)

            return list(zip(timestamp, volume))

    def get_market_cap_financial_data(self, currency):
        with open(os.path.join(self.data_path, currency + ".csv"), "r") as file:
            reader = csv.reader(file)
            data = list(file)
            data.pop(0)
            timestamp, usd, btc, volume = zip(*data)
            timestamp = map(int, timestamp)
            volume = map(int, volume)

            return list(zip(timestamp, ))

    def get_currencies_from_file_names(self, size_limit=math.inf):
        output = []
        for index, filename in enumerate(os.listdir(self.data_path)):
            if index == size_limit:
                return output

            output.append(filename.split(".")[0])

        return output

    def get_return_data(self, currency):
        input = self.get_financial_data(currency)

        output = []
        for index, element in enumerate(input):
            if index == 0:
                continue
            output.append((element[0], (element[1] / input[index - 1][1]) - 1))

        return output

    @staticmethod
    def return_data_to_dict(data):
        output = {}
        for timestamp, datapoint in data:
            output[timestamp] = datapoint

        return output


run_script = Currency()
# run_script.get_return_correlation_data("bitcoin", "ethereum")
# run_script.get_return_correlation_data("bitcoin", "litecoin")
# run_script.get_return_correlation_data("ethereum", "litecoin")
# run_script.get_return_correlation_data("ripple", "litecoin")
# run_script.get_return_correlation_data("ripple", "bitcoin")
# run_script.get_return_correlation_data("ripple", "ethereum")
# run_script.get_all_correlations()
