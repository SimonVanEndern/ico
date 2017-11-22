import csv

from common.currency import Currency
from common.currency_handler import CurrencyHandler
from google_trends.import_data.google_trends_DTO import GoogleTrendsDTO


class TotalCSVExport:
    currency_handler = CurrencyHandler.Instance()

    def __init__(self):
        with open("crypto-currency-export-until-31-10-2017.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")
            writer.writerow(["Crypto-currency name", "Timestamp", "Volume", "Market Capitalization", "Price in USD",
                             "Google Trends reltative change 12 hours ago"])

            for currency_name in self.currency_handler.get_all_currency_names():
                currency: Currency = self.currency_handler.get_currency(currency_name)

                google_trends_relative_data = GoogleTrendsDTO(currency_name).load_aggregated_data()
                google_trends_dict = dict()

                if google_trends_relative_data is None:
                    google_trends_relative_data = ""
                else:
                    for element in google_trends_relative_data:
                        google_trends_dict[(element[0] + 12 * 3600) * 1000] = element[1]

                for index in currency.data.index:
                    gtd_data = ""
                    if index in google_trends_dict:
                        gtd_data = google_trends_dict[index]

                    writer.writerow([currency_name,
                                     index,
                                     currency.data["volume"][index],
                                     currency.data["market_cap"][index],
                                     currency.data["usd"][index],
                                     gtd_data])


TotalCSVExport()
