import logging

from csv_strings import CSVStrings
from finance.compressed_raw_data import datapoint_dto


class CurrencyDTO:
    def __init__(self, currency):
        self.currency = currency
        self.data = {}

    def to_csv(self):
        csv = []
        for key, value in self.data.items():
            csv.append((value.timestamp, value.usd, value.btc, value.volume, value.market_cap))

        csv.sort()
        csv.insert(0, ("Timestamp", "USD", "BTC", "Volume", "Market_cap"))

        return csv

    def add_data(self, raw_json_data):
        data = self.extract_data(raw_json_data)

        for key, value in data.items():
            if key in self.data:
                if self.data[key] != value:
                    print(self.data[key])
                    print(value)
                    raise Exception("Different double value")

            self.data[key] = value

    def extract_data(self, data):
        output = {}

        market_cap = list(data[CSVStrings.market_cap_string])
        price_usd = list(data[CSVStrings.price_usd_string])
        price_btc = list(data[CSVStrings.price_btc_string])
        volume_usd = list(data[CSVStrings.volume_string])

        for capitalization in market_cap:
            datapoint = datapoint_dto.from_market_cap(capitalization)
            output[datapoint.timestamp] = datapoint

        for price in price_usd:
            if int(price[0]) in output:
                output[int(price[0])].add_usd(price)
            else:
                logging.info("{}: Different timelines".format(self.__class__.__name__))
                datapoint = datapoint_dto.from_usd(price)
                output[datapoint.timestamp] = datapoint

        for price in price_btc:
            if int(price[0]) in output:
                output[int(price[0])].add_btc(price)
            else:
                logging.info("{}: Different timelines".format(self.__class__.__name__))
                datapoint = datapoint_dto.from_btc(price)
                output[datapoint.timestamp] = datapoint

        for volume in volume_usd:
            if int(volume[0]) in output:
                output[int(volume[0])].add_volume(volume)
            else:
                logging.info("{}: Different timelines".format(self.__class__.__name__))
                datapoint = datapoint_dto.from_volume(volume)
                output[datapoint.timestamp] = datapoint

        return output
