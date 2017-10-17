import logging
from datetime import datetime, timedelta

from finance.raw_data.coinmarketcap_importer import CoinMarketCapGraphAPIImporter


class FinancialDataCalculator:
    def __init__(self):
        self.missing_data = {}
        self.raw_data_importer = CoinMarketCapGraphAPIImporter()
        pass

    def calculate_for_timestamp(self, timestamp, data_before, data_after):
        output = data_before["data"].copy()
        for index, value in enumerate(output):
            difference_data = data_after["data"][index] - data_before["data"][index]
            difference_time = data_after["time"] - data_before["time"]
            slope = difference_data / difference_time
            output[index] += slope * (timestamp - data_before["time"])

        output = list(map(lambda x: format(x, '.2f'), output))
        return {'time': timestamp, 'data': output}

    # End is excluded
    def calculate_series_for_timestamp(self, start, end, step, data, currency, maximum_timespan=1):  #
        self.missing_data[currency] = []
        current_data_index = 0
        output = []
        for timestamp in range(start, end, step):
            while not (data[current_data_index]["time"] <= timestamp <= data[current_data_index + 1]["time"]):
                current_data_index += 1

                if current_data_index + 1 >= len(data):
                    print(self.missing_data[currency])
                    self.get_missing_data(currency)
                    return output

            timespan = (data[current_data_index + 1]["time"] - data[current_data_index]["time"]) / 1000 / 3600
            if timespan > maximum_timespan:
                self.missing_data[currency].append(
                    (data[current_data_index]["time"], data[current_data_index + 1]["time"]))
                current_data_index += 1
                logging.warning(
                    "No sufficient data for timestamp {}. Timespan in hours is {}".format(timestamp, timespan))
                continue

            calculated_data = self.calculate_for_timestamp(timestamp, data[current_data_index],
                                                           data[current_data_index + 1])
            output.append(calculated_data)

        print(self.missing_data[currency])
        self.get_missing_data(currency)

        return output

    def get_missing_data(self, currency):
        if len(self.missing_data[currency]) > 0:
            self.raw_data_importer.request_additional_data(currency, self.missing_data[currency])


def get_next_timestamp_at_time(timestamp, hours):
    date = datetime.fromtimestamp(timestamp / 1e3)
    if date.hour < hours:
        new_date = date.replace(hour=hours, minute=0, second=0)
    else:
        new_date = date + timedelta(days=1)
        new_date = new_date.replace(hour=hours, minute=0, second=0)

    return int(new_date.timestamp() * 1e3)


def get_last_timestamp_at_time(timestamp, hours):
    date = datetime.fromtimestamp(timestamp / 1e3)
    if date.hour >= hours:
        new_date = date.replace(hour=hours, minute=0, second=0)
    else:
        new_date = date - timedelta(days=1)
        new_date = new_date.replace(hour=hours, minute=0, second=0)

    return int(new_date.timestamp() * 1e3)
