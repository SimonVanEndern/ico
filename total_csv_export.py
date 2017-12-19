import csv

import numpy

from common.currency import Currency
from common.currency_handler import CurrencyHandler
from google_trends.import_data.google_trends_DTO import GoogleTrendsDTO


class TotalCSVExport:
    currency_handler = CurrencyHandler.Instance()

    def __init__(self):
        with open("crypto-currency-export-until-31-11-2017-daily-with-google-trends-data.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["Crypto-currency name", "Timestamp", "Volume", "Market Capitalization", "Price in USD",
                             "Google Trends relatative change 12 hours ago"])

            # counter = 0
            for currency_name in self.currency_handler.get_all_currency_names():
                # counter += 1
                # if counter > 10:
                #     break
                currency: Currency = self.currency_handler.get_currency(currency_name)
                if currency is None or currency.data is None:
                    print("Currency somehow not there")
                    continue

                google_trends_relative_data = GoogleTrendsDTO(currency_name).load_aggregated_data()
                google_trends_dict = dict()

                if google_trends_relative_data is not None:
                    for element in google_trends_relative_data:
                        google_trends_dict[(element[0] + 12 * 3600) * 1000] = element[1]

                for index in currency.data.index:
                    gtd_data = numpy.nan
                    if index in google_trends_dict:
                        gtd_data = google_trends_dict[index]

                    writer.writerow([currency_name,
                                     index,
                                     currency.data["volume"][index],
                                     currency.data["market_cap"][index],
                                     currency.data["usd"][index],
                                     gtd_data])


TotalCSVExport()
