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
folderPath = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"

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
for idx, symbol in enumerate(tickerSymbols):
    # if idx == 10:
    #     break

    try:
        path = folderPath + symbol + ".csv"
        if os.path.isfile(path):
            print("Already exists: " + path)
            continue

        conn = http.client.HTTPSConnection(basicUrl)
        conn.request("GET", "/currencies/" + symbol + "/")

        response = conn.getresponse()
        data = json.loads(response.read().decode("UTF-8"))

        exporter.export(data, folderPath + symbol + ".csv")

        time.sleep(10)

    except json.decoder.JSONDecodeError as ex:
        print(ex)
        print("Exception: " + symbol)
        time.sleep(10)
