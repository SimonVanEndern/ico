import datetime
import http.client
import json
import logging
import os.path
import time

from finance.coursedata import exporter

logging.basicConfig(level=logging.DEBUG)

# http.client.HTTPSConnection.debuglevel = 1

# Variables to be used
times = []
currencies = []
tickerSymbols = []
data = []

basicUrl = "graphs.coinmarketcap.com"
folderPath = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-10\\"

# Get currently supported currencies
conn = http.client.HTTPSConnection("api.coinmarketcap.com")
conn.request("GET", "/v1/ticker/")

response = conn.getresponse()

currencies = json.loads(response.read().decode("UTF-8"))

# Get ticker symbol of currencies for requests.
for currency in currencies:
    tickerSymbols.append(currency["id"])

if tickerSymbols[0] != "bitcoin":
    print("Error")
    print(tickerSymbols[0])

exporter = exporter.Exporter()

# GetData
# for idx, symbol in enumerate(tickerSymbols):
#     # if idx == 10:
#     #     break
#
#     try:
#         path = folderPath + symbol + ".csv"
#         if os.path.isfile(path):
#             print("Already exists: " + path)
#             continue
#
#         conn = http.client.HTTPSConnection(basicUrl)
#         conn.request("GET", "/currencies/" + symbol + "/")
#
#         response = conn.getresponse()
#         data = json.loads(response.read().decode("UTF-8"))
#
#         exporter.export(data, folderPath + symbol + ".csv")
#
#         time.sleep(10)
#
#     except json.decoder.JSONDecodeError as ex:
#         print(ex)
#         print("Exception: " + symbol)
#         time.sleep(10)


class CoinmarketcapImportFinanceData:
    basicUrl = "graphs.coinmarketcap.com"
    price_usd_string = "price_usd"

    def request_currency(self, currency):
        conn = http.client.HTTPSConnection(basicUrl)
        path = "/currencies/{}/".format(currency)
        conn.request("GET", path)

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))

        datapoints = data[self.price_usd_string]

        first_date = datapoints[0][0]
        # print(first_date)
        last_date = datapoints[len(datapoints) - 1][0]
        end_date = first_date + 365 * 24 * 60 * 60 * 1000

        if not self.validate_data(data, path):
            self.request_data_monthly(currency, first_date, last_date)

        return data

    def request_data(self, symbol, start, end):
        print("Sleeping for 10 secs")
        time.sleep(10)
        conn = http.client.HTTPSConnection(basicUrl)
        path = "/currencies/{}/{}/{}/".format(symbol, start, end)
        conn.request("GET", path)

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))

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

    def request_data_monthly(self, currency, first_date, last_date):
        time_month = 30 * 24 * 60 * 60 * 1000

        start = first_date
        while start + time_month < last_date:
            data = self.request_data(currency, start, start + time_month)
            self.validate_data(data, "quarterly/" + str(start) + "/" + str(start + time_month))
            start += time_month

        data = self.request_data(currency, start, last_date)
        self.validate_data(data, "quarterly/" + str(start))


run_script = CoinmarketcapImportFinanceData()
run_script.request_currency("bitcoin")
