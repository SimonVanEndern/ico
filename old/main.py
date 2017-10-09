import logging

logging.basicConfig(level=logging.DEBUG)

import http.client
import json
from _datetime import datetime

# http.client.HTTPSConnection.debuglevel = 1

# Variables to be used
times = []
currencies = []
tickerSymbols = []
data = []

basicUrl = "graphs.coinmarketcap.com"

# Crate start and end date for requests
for i in range(0, 4):
    time = {}
    time['start'] = datetime.strptime("01.01." + str(2013 + i), "%d.%m.%Y").timestamp()*1000
    time['end'] = datetime.strptime("31.12." + str(2013 + i), "%d.%m.%Y").timestamp()*1000
    times.append(time)

if times[0]["start"] != 1356994800000:
    print("Error")
    print(times)


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

# GetData
for idx, symbol in enumerate(tickerSymbols):
    conn = http.client.HTTPSConnection(basicUrl)
    conn.request("GET", "/currencies/" + symbol + "/" + str(int(times[3]["start"])) + "/" + str(int(times[3]["end"])) + '/')

    response = conn.getresponse()
    datapoint = {}
    datapoint["id"] = symbol
    datapoint["data"] = response.read().decode("UTF-8")
    print(datapoint)
    data.append(datapoint)
    if idx == 10:
        break

with open('output.txt', 'w') as outfile:
    json.dump(data, outfile)