import datetime
import http.client
import json
import logging
import os.path
import time

from global_data import GlobalData

logging.basicConfig(level=logging.DEBUG)


# exporter = exporter.Exporter()

# ToDo: Automatically reduce received data (timestamp is there for any datapoint)


class CoinmarketcapImportFinanceData:
    basicUrl = "graphs.coinmarketcap.com"
    price_usd_string = "price_usd"

    save_path = GlobalData.download_raw_data_path_external
    last_timestamp = GlobalData.last_date_for_download

    save_path_additional_data = GlobalData.save_path_additional_data

    def request_currency(self, currency):
        # ToDO: Replace this request with a request to the currency_handler module. Each currency should
        # have an attribute for the start date
        conn = http.client.HTTPSConnection(self.basicUrl)
        path = "/currencies/{}/".format(currency)
        conn.request("GET", path)

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))

        datapoints = data[self.price_usd_string]

        first_date = datapoints[0][0]
        # last_date = datapoints[len(datapoints) - 1][0]
        last_date = self.last_timestamp

        if not os.path.isdir(os.path.join(self.save_path, currency)):
            os.mkdir(os.path.join(self.save_path, currency))

        self.request_data_monthly(currency, first_date, last_date)

        open(os.path.join(self.save_path, currency, "ready.txt"), "w").close()

    def request_data_monthly(self, currency, first_date, last_date):
        time_month = 29 * 24 * 60 * 60 * 1000

        start = first_date
        while start + time_month < last_date:
            data = self.request_data(currency, start, start + time_month, self.save_path)
            self.save_data(data, currency, start, start + time_month, self.save_path)

            start += time_month

        data = self.request_data(currency, start, last_date, self.save_path)
        self.save_data(data, currency, start, last_date, self.save_path)

    def request_data(self, currency, start, end, save_path):
        if self.check_data_already_downloaded(currency, start, end, save_path):
            return None
        print("Sleeping for 1 secs")
        time.sleep(1)
        conn = http.client.HTTPSConnection(self.basicUrl)
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
        else:
            logging.info("{} saved data from {} to {} --> {} entries".format(self.__class__.__name__, start, end,
                                                                             len(data[self.price_usd_string])))
            if len(data[self.price_usd_string]) < 800:
                logging.warning(
                    "For {} to {} we only got {} entries".format(start, end, len(data[self.price_usd_string])))

            filename = str(start) + "-" + str(end) + ".json"
            if not os.path.isdir(os.path.join(path, currency)):
                os.mkdir(os.path.join(path, currency))

            with open(os.path.join(path, currency, filename), "w") as file:
                json.dump(data, file)

    def check_data_already_downloaded(self, currency, start, end, save_path):
        filename = str(start) + "-" + str(end) + ".json"
        return os.path.isfile(os.path.join(save_path, currency, filename))

    def request_additional_data(self, currency, timespan_tuples):
        for timespan in timespan_tuples:
            data = self.request_data(currency, timespan[0], timespan[1], self.save_path_additional_data)
            self.save_data(data, currency, timespan[0], timespan[1], self.save_path_additional_data)
