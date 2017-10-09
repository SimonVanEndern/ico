import http.client
import json


class CoinmarketCap:
    def __init__(self):
        conn = http.client.HTTPSConnection("api.coinmarketcap.com")
        conn.request("GET", "/v1/ticker/")

        response = conn.getresponse()

        currencies = json.loads(response.read().decode("UTF-8"))

    def getCurrencies(self):
        tickerSymbols = []

        # Get ticker symbol of currencies for requests.
        for currency in self.currencies:
            tickerSymbols.append(currency["id"])
        return tickerSymbols