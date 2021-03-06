import logging

from csv_strings import CSVStrings
from finance_data_import.compressed_raw_data import datapoint_dto


class CurrencyDTO:
    def __init__(self, currency):
        self.currency = currency
        self.data = {}

    def to_csv(self):
        csv = list()

        if len(self.data) == 0:
            raise Exception("Currency {}: no financial data calculated".format(self.currency))

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
                    if self.data[key] != 0 and value != 0:
                        raise Exception("Different double value")

            self.data[key] = value

    def extract_data(self, data):
        output = {}

        market_cap = list(data[CSVStrings.MARKET_CAP_STRING])
        price_usd = list(data[CSVStrings.PRICE_USD_STRING])
        price_btc = list(data[CSVStrings.PRICE_BTC_STRING])
        volume_usd = list(data[CSVStrings.VOLUME_STRING])

        for capitalization in market_cap:
            datapoint = datapoint_dto.from_market_cap(capitalization)
            if datapoint.timestamp in output:
                if datapoint != output[datapoint.timestamp]:
                    print(datapoint)
                    print(output[datapoint.timestamp])
                    raise Exception("Different data for same time")
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
