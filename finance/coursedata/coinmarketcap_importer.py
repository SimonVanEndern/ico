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

    save_path = GlobalData.download_data_path_external

    def request_currency(self, currency):
        conn = http.client.HTTPSConnection(basicUrl)
        path = "/currencies/{}/".format(currency)
        conn.request("GET", path)

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))

        datapoints = data[self.price_usd_string]

        first_date = datapoints[0][0]
        last_date = datapoints[len(datapoints) - 1][0]

        if not os.path.isdir(os.path.join(self.save_path, currency)):
            os.mkdir(os.path.join(self.save_path, currency))

        self.request_data_monthly(currency, first_date, last_date)

    def request_data_monthly(self, currency, first_date, last_date):
        time_month = 29 * 24 * 60 * 60 * 1000

        start = first_date
        while start + time_month < last_date:
            data = self.request_data(currency, start, start + time_month)
            self.save_data(data, currency, start, start + time_month)

            start += time_month

        data = self.request_data(currency, start, last_date)
        self.save_data(data, currency, start, last_date)

    def request_data(self, symbol, start, end):
        print("Sleeping for 2 secs")
        time.sleep(2)
        conn = http.client.HTTPSConnection(self.basicUrl)
        path = "/currencies/{}/{}/{}/".format(symbol, start, end)
        conn.request("GET", path)

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))
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

    def save_data(self, data, currency, start, end):
        logging.info("{} saved data from {} to {} --> {} entries".format(self.__class__.__name__, start, end,
                                                                         len(data[self.price_usd_string])))
        if len(data[self.price_usd_string]) < 800:
            logging.warning(
                "For {} to {} we only got {} entries".format(start, end, len(data[self.price_usd_string])))

        filename = str(start) + "-" + str(end) + ".json"
        with open(os.path.join(self.save_path, currency, filename), "w") as file:
            json.dump(data, file)
