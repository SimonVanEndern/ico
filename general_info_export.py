import csv

from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency_handler import CurrencyHandler


class GeneralInfoExport:
    cf: CurrencyHandler = CurrencyHandler.Instance()
    tp: CoinmarketCapTokenParser = CoinmarketCapTokenParser()

    def __init__(self):
        all_currencies_names = self.cf.get_all_currency_names()
        all_currencies = list(map(lambda x: self.cf.get_currency(x), all_currencies_names))
        for currency in all_currencies:
            currency.get_statistical_data()

        with open("export_general_information.csv", "w") as file:
            writer = csv.writer(file, delimiter=",", lineterminator="\n")

            writer.writerow(["Crypto-currency",
                             "Start Timestamp",
                             "Keyword 'coin'",
                             "Keyword 'token'",
                             "Keyword 'bit'",
                             "Token",
                             "Coin",
                             "Platform"])

            for currency in all_currencies:
                if currency.currency == "ethereum":
                    x=7
                writer.writerow([currency.currency,
                                 currency.statistical_data.first_date,
                                 currency.contains_keyword("coin"),
                                 currency.contains_keyword("token"),
                                 currency.contains_keyword("bit"),
                                 self.tp.is_token(currency.currency),
                                 self.tp.is_coin(currency.currency),
                                 self.tp.is_platform(currency.currency)])


GeneralInfoExport()
