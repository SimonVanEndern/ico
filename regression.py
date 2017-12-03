from datetime import datetime
from pprint import pprint

import numpy
import pandas
from statsmodels.formula.api import ols

from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency_handler import CurrencyHandler


class Regression:
    ch = CurrencyHandler.Instance()

    def __init__(self):
        self.all_currency_names = self.ch.get_all_currency_names()
        self.all_currencies = list(map(lambda x: self.ch.get_currency(x), self.all_currency_names))
        for currency in self.all_currencies:
            currency.get_statistical_data()

        self.data: pandas.DataFrame = pandas.DataFrame([1])
        self.currencies_3_months = list()

    def run(self):
        tokens = CoinmarketCapTokenParser().get_all_tokens()
        tokens = list(map(lambda x: x["currency"], tokens))
        tokens = list(map(lambda x: self.ch.get_currency(x), tokens))
        token_vs_coin = list(map(lambda x: x in tokens, self.all_currencies))
        token_vs_coin = pandas.DataFrame(token_vs_coin).astype(int)
        token_vs_coin.columns = ["token"]
        token_vs_coin = list(token_vs_coin["token"])
        print(token_vs_coin)
        # print(token_vs_coin.as_type(int))
        print(sum(token_vs_coin))

        keyword_dummy = list(map(lambda x: x.contains_keyword("any"), self.all_currencies))
        keyword_dummy = pandas.DataFrame(keyword_dummy).astype(int)
        keyword_dummy.columns = ["keyword"]
        keyword_dummy = list(keyword_dummy["keyword"])

        initial_price = list(map(lambda x: x.statistical_data.first_price, self.all_currencies))
        log_initial_price = list(map(lambda x: numpy.log(x), initial_price))
        initial_price_rank = pandas.DataFrame(initial_price).rank()
        initial_price_rank.columns = ["initial"]
        initial_price_rank = list(initial_price_rank["initial"])
        initial_price_median = numpy.nanmedian(initial_price)
        initial_price_binary = list(map(lambda x: 1 if x > initial_price_median else 0, initial_price))

        start_dates = list(map(lambda x: x.statistical_data.first_date, self.all_currencies))
        start_dates = list(numpy.array(start_dates) - min(start_dates))
        start_dates_rank = pandas.DataFrame(start_dates).rank()
        start_dates_rank.columns = ["start"]
        start_dates_rank = list(start_dates_rank["start"])
        start_dates_median = numpy.nanmedian(start_dates)
        start_dates_binary = list(map(lambda x: 1 if x > start_dates_median else 0, start_dates))

        volumes = list(map(lambda x: x.statistical_data.average_volume, self.all_currencies))
        log_volumes = list(map(lambda x: numpy.log(x), volumes))
        volumes_rank = pandas.DataFrame(volumes).rank()
        volumes_rank.columns = ["volumes"]
        volumes_rank = list(volumes_rank["volumes"])
        volumes_median = numpy.nanmedian(volumes)
        volumes_binary = list(map(lambda x: 1 if x > volumes_median else 0, volumes))

        market_caps = list(map(lambda x: x.statistical_data.average_market_capitalization, self.all_currencies))
        log_market_caps = list(map(lambda x: numpy.log(x) if numpy.isfinite(x) and x > 0 else 0, market_caps))
        market_caps_rank = pandas.DataFrame(market_caps).rank()
        market_caps_rank.columns = ["mcaps"]
        market_caps_rank = list(market_caps_rank["mcaps"])
        market_caps_median = numpy.nanmedian(market_caps)
        market_caps_binary = list(map(lambda x: 1 if x > market_caps_median else 0, market_caps))

        self.currencies_3_months = list(
            map(lambda x: self.ch.get_currency(x, datetime.strptime("01.08.2017", "%d.%m.%Y")),
                self.all_currency_names))
        for currency in self.currencies_3_months:
            currency.get_statistical_data()

        market_caps_3_months = list(
            map(lambda
                    x: x.statistical_data.average_market_capitalization if x.statistical_data is not None else numpy.nan,
                self.currencies_3_months))
        log_market_caps_3_months = list(
            map(lambda x: numpy.log(x) if numpy.isfinite(x) and x > 0 else 0, market_caps_3_months))
        market_caps_rank_3_months = pandas.DataFrame(market_caps_3_months).rank()
        market_caps_rank_3_months.columns = ["mcaps"]
        market_caps_rank_3_months = list(market_caps_rank_3_months["mcaps"])
        market_caps_3_months_median = numpy.nanmedian(market_caps)
        market_caps_3_months_binary = list(
            map(lambda x: 1 if x > market_caps_3_months_median else 0, market_caps_3_months))

        volumes_3_months = list(
            map(lambda x: x.statistical_data.average_volume if x.statistical_data is not None else numpy.nan,
                self.currencies_3_months))
        log_volumes_3_months = list(map(lambda x: numpy.log(x) if numpy.isfinite(x) and x > 0 else 0, volumes_3_months))
        volumes_rank_3_months = pandas.DataFrame(volumes_3_months).rank()
        volumes_rank_3_months.columns = ["volumes"]
        volumes_rank_3_months = list(volumes_rank_3_months["volumes"])
        volumes_3_months_median = numpy.nanmedian(volumes)
        volumes_3_months_binary = list(map(lambda x: 1 if x > volumes_3_months_median else 0, volumes_3_months))

        combined = numpy.array(volumes) / numpy.array(market_caps)
        combined[numpy.isinf(combined)] = numpy.nan
        velocity = combined

        velocity_rank = pandas.DataFrame(velocity).rank()
        velocity_rank.columns = ["velocity"]
        velocity_rank = list(velocity_rank["velocity"])

        returns = list(map(lambda x: x.statistical_data.price_change, self.all_currencies))
        log_returns = list(map(lambda x: numpy.log(x) if numpy.isfinite(x) and x > 0 else 0, returns))
        returns_rank = pandas.DataFrame(returns).rank()
        returns_rank.columns = ["returns"]
        returns_rank = list(returns_rank["returns"])
        returns_median = numpy.nanmedian(returns)
        returns_binary = list(map(lambda x: 1 if x > returns_median else 0, returns))

        self.data = pandas.DataFrame(
            {"keyword": keyword_dummy, "token": token_vs_coin, "initial_price_rank": initial_price_rank,
             "volumes_rank": volumes_rank, "market_caps_rank": market_caps_rank, "initial_prices": initial_price,
             "volumes": volumes, "market_caps": market_caps, "velocity": velocity, "returns": returns,
             "returns_rank": returns_rank, "market_caps_rank_3_months": market_caps_rank_3_months,
             "market_caps_3_months": market_caps_3_months, "volumes_rank_3_months": volumes_rank_3_months,
             "volumes_3_months": volumes_3_months, "velocity_rank": velocity_rank, "log_volumes": log_volumes,
             "log_volumes_3_months": log_volumes_3_months, "log_returns": log_returns,
             "log_market_caps": log_market_caps, "log_market_caps_3_months": log_market_caps_3_months,
             "log_initial_price": log_initial_price, "start_dates": start_dates, "start_dates_rank": start_dates_rank,
             "initial_price_binary": initial_price_binary, "start_dates_binary": start_dates_binary,
             "volumes_binary": volumes_binary, "market_caps_binary": market_caps_binary,
             "market_caps_3_months_binary": market_caps_3_months_binary,
             "volumes_3_months_binary": volumes_3_months_binary, "returns_binary": returns_binary})

    def find_regression(self):
        outcomes = list()
        y_values = ["market_caps_3_months", "log_market_caps", "market_caps_rank", "market_caps",
                    "returns", "returns_rank", "market_caps_rank_3_months", "log_returns", "log_market_caps",
                    "log_market_caps_3_months"]

        for y_value in y_values:
            for variable in self.data.keys():
                # if variable not in y_values:
                equation = y_value + " ~ " + variable
                outcomes.append((equation, ols(equation, self.data).fit().rsquared))

        outcomes.sort(key=lambda x: x[1])
        pprint(outcomes)

    def print_regressions(self):
        print("Overall Returns rank")
        print(ols("returns_rank ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword",
            self.data).fit().summary())

        print("Returns binary")
        print(ols("returns_binary ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword",
            self.data).fit().summary())

        print("Returns binary")
        print(ols("returns_binary ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword + initial_price_binary",
            self.data).fit().summary())

        print("Market caps rank 3 months")
        print(ols("market_caps_rank_3_months ~ token + keyword + initial_price_rank + start_dates_rank + start_dates_binary + start_dates",
                  self.data).fit().summary())

        print("Volume rank 3 months")
        print(ols("volumes_rank_3_months ~ token + keyword + initial_price_rank + start_dates_rank + start_dates_binary + start_dates",
                  self.data).fit().summary())

        print("Market cap")
        print(ols("market_caps_3_months ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword",
            self.data).fit().summary())

        print("Volume")
        print(ols("volumes_3_months ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword",
            self.data).fit().summary())

        print("Market caps rank 3 months through market caps rank")
        print(ols("market_caps_rank_3_months ~  market_caps_rank", self.data).fit().summary())

        print("Market caps 3 months through market caps")
        print(ols("market_caps_3_months ~ market_caps", self.data).fit().summary())

        print("Volumes rank 3 months through volumes rank")
        print(ols("volumes_rank_3_months ~ volumes_rank", self.data).fit().summary())

        print("Volumes 3 months through volumes")
        print(ols("volumes_3_months ~ volumes", self.data).fit().summary())

        print("Volumes 3 months through market caps")
        print(ols("volumes_3_months ~ market_caps", self.data).fit().summary())

        print("Market caps 3 months through volumes")
        print(ols("market_caps_3_months ~ volumes", self.data).fit().summary())


        print("Returns rank market caps rank + volumes rank")
        print(ols(
            "returns_rank ~ initial_price_rank + start_dates_rank + token + start_dates_binary + start_dates + keyword + market_caps_rank + volumes_rank",
            self.data).fit().summary())

        print("Log returns")
        print(ols(
            "log_returns ~ initial_price_rank + log_initial_price + start_dates_rank + start_dates_binary + token + keyword",
            self.data).fit().summary())

        print("Log returns including volume")
        print(ols(
            "log_returns ~ initial_price_rank + log_initial_price + start_dates_rank + start_dates_binary + token + keyword + volumes_rank + volumes_binary + log_volumes",
            self.data).fit().summary())

        print("Log returns including volume and market cap")
        print(ols(
            "log_returns ~ initial_price_rank + log_initial_price + start_dates_rank + start_dates_binary + token + keyword + volumes_rank + volumes_binary + log_volumes + market_caps_rank + market_caps",
            self.data).fit().summary())

        print("Log returns including volume and market cap and velocity")
        print(ols(
            "log_returns ~ initial_price_rank + log_initial_price + start_dates_rank + start_dates_binary + token + keyword + volumes_rank + volumes_binary + log_volumes + market_caps_rank + market_caps + velocity_rank",
            self.data).fit().summary())

        print("Log returns including volume and market cap and velocity and velocity rank")
        print(ols(
            "log_returns ~ initial_price_rank + log_initial_price + start_dates_rank + start_dates_binary + token + keyword + volumes_rank + volumes_binary + log_volumes + market_caps_rank + market_caps + velocity_rank + velocity",
            self.data).fit().summary())

        print("Market caps rank 3 months including velocity")
        print(ols(
            "market_caps_rank_3_months ~ token + keyword + initial_price_rank + start_dates_rank + start_dates_binary + velocity_rank",
            self.data).fit().summary())

        print("Market caps 3months velocity and volumes rank")
        print(ols(
            "market_caps_rank_3_months ~ token + keyword + initial_price_rank + start_dates_rank + start_dates_binary + velocity_rank + volumes_rank_3_months",
            self.data).fit().summary())

        print("volumes 3 months through volumes + market caps")
        print(ols("volumes_3_months ~ volumes + market_caps", self.data).fit().summary())


regression = Regression()
regression.run()
regression.print_regressions()
