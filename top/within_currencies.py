from datetime import datetime

from common.currency import Currency
from common.currency_handler import CurrencyHandler


class WithinCurrencies:
    def __init__(self, start_date: datetime):
        self.start_date:datetime = start_date
        self.currency_handler: CurrencyHandler = CurrencyHandler()
        self.data: dict = dict()

    def get_data(self):
        for currency in self.currency_handler.get_all_currency_names():
            handle_on_currency: Currency = self.currency_handler.get_currency(currency, date_limit=self.start_date)
            self.data[currency] = handle_on_currency.get_statistical_data()

        return self.data

            # Correlation between Volume and return
            # Each time 3,2,1 day after / before shift
            # Correlation between market capitalization change and price change

            # Correlation with google search data

            # Total volume
            # Average volume
            # Volume linear regression

            # Average market capitalization
            # Market cap linear regression

            # Average price
            # price linear regression

            # highest / lowest price
            # price change from beginning on

            # volatility
            # linear regression on volatility

            # percentage of total market capitalization according to coinmarketcap
