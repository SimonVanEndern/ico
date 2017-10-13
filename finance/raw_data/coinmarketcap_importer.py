import datetime
import http.client
import json
import logging
import os.path
import time

from csv_strings import CSVStrings
from global_data import GlobalData

logging.basicConfig(level=logging.DEBUG)


# exporter = exporter.Exporter()

# ToDo: Automatically reduce received data (timestamp is there for any datapoint)


def get_basic_currency_data(currency):
    # ToDO: Handle this request with a different module
    conn = http.client.HTTPSConnection(GlobalData.coin_market_cap_graph_api_url)
    path = "/currencies/{}/".format(currency)
    conn.request("GET", path)

    response = conn.getresponse()
    data = json.loads(response.read().decode("UTF-8"))

    datapoints = data[CSVStrings.price_usd_string]

    return {"start_date": datapoints[0][0]}


def check_data_already_downloaded(currency, start, end, save_path):
    filename = str(start) + "-" + str(end) + ".json"
    return os.path.isfile(os.path.join(save_path, currency, filename))


class CoinMarketCapGraphAPIImporter:
    def __init__(self):
        self.coin_market_cap_graph_api_url = GlobalData.coin_market_cap_graph_api_url

        self.price_usd_string = CSVStrings.price_usd_string

        self.raw_data_path = GlobalData.download_raw_data_path_external
        self.save_path_additional_data = GlobalData.save_path_additional_data

        self.last_timestamp = GlobalData.last_date_for_download

    def request_currency(self, currency):
        basic_currency_data = get_basic_currency_data(currency)
        first_date = basic_currency_data["start_date"]

        last_date = self.last_timestamp

        if not os.path.isdir(os.path.join(self.raw_data_path, currency)):
            os.mkdir(os.path.join(self.raw_data_path, currency))

        self.request_data_monthly(currency, first_date, last_date)

        open(os.path.join(self.raw_data_path, currency, "ready.txt"), "w").close()

    def request_data_monthly(self, currency, first_date, last_date):
        span_month = 29 * 24 * 60 * 60 * 1000

        start = first_date
        while start + span_month < last_date:
            data = self.request_data(currency, start, start + span_month, self.raw_data_path)
            self.save_data(data, currency, start, start + span_month, self.raw_data_path)

            start += span_month

        data = self.request_data(currency, start, last_date, self.raw_data_path)
        self.save_data(data, currency, start, last_date, self.raw_data_path)

    def request_data(self, currency, start, end, save_path):
        if check_data_already_downloaded(currency, start, end, save_path):
            return None

        print("Sleeping for 1 secs")
        time.sleep(1)
        conn = http.client.HTTPSConnection(self.coin_market_cap_graph_api_url)
        path = "/currencies/{}/{}/{}/".format(currency, start, end)
        conn.request("GET", path)

        response = conn.getresponse()
        try:
            data = json.loads(response.read().decode("UTF-8"))
        except json.decoder.JSONDecodeError:
            data = None
            logging.warning("No results: {}".format(path))
        conn.close()

        return data

    def validate_data(self, data, path):
        last = data[self.price_usd_string][0][0]
        for timestamp, price in data[self.price_usd_string]:
            if timestamp - last > 24 * 60 * 60 * 1000:
                print(path)
                print("Error: too few time")
                print(timestamp - last)
                print(datetime.datetime.fromtimestamp(timestamp / 1e3))
                return False
            last = timestamp

    def save_data(self, data, currency, start, end, path):
        if data is None:
            logging.info(
                "{}: Currency {} from {} to {} already downloaded".format(self.__class__.__name__, currency, start,
                                                                          end))
            return

        if len(data[self.price_usd_string]) == 2:
            logging.info(
                "{}: Currency {} from {} to {} has no additional data".format(self.__class__.__name__, currency, start,
                                                                              end))
            return

        else:
            logging.info("{}: saved data from {} to {} --> {} entries".format(self.__class__.__name__, start, end,
                                                                              len(data[self.price_usd_string])))
            if len(data[self.price_usd_string]) < 800:
                logging.warning(
                    "For {} to {} we only got {} entries".format(start, end, len(data[self.price_usd_string])))

            filename = str(start) + "-" + str(end) + ".json"
            if not os.path.isdir(os.path.join(path, currency)):
                os.mkdir(os.path.join(path, currency))

            with open(os.path.join(path, currency, filename), "w") as file:
                json.dump(data, file)

    def request_additional_data(self, currency, time_span_tuples):
        for time_span in time_span_tuples:
            data = self.request_data(currency, time_span[0], time_span[1], self.save_path_additional_data)
            self.save_data(data, currency, time_span[0], time_span[1], self.save_path_additional_data)
