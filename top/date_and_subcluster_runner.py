import os
import shutil
from datetime import datetime
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt
import pandas

from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser
from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from global_data import GlobalData
from top.clustered_plot_and_data_exporter import ClusteredStatisticalAnalysisRunnerAndExporter
from top.plot_and_data_exporter import StatisticalAnalysisRunnerAndExporter
from top.within_currencies import WithinCurrencies


class DateAndSubClusterRunner:

    coinmarketcap_coins = CoinmarketCapCoinParser()
    coinmarketcap_tokens = CoinmarketCapTokenParser()

    def __init__(self):
        self.currency_handler = CurrencyHandler.Instance()

        # Start Dates of Time Series
        self.start_total: datetime = None
        self.start_2017: datetime = datetime.strptime("01.01.2017", "%d.%m.%Y")
        self.month_6: datetime = datetime.strptime("01.05.2017", "%d.%m.%Y")
        self.month_3: datetime = datetime.strptime("01.08.2017", "%d.%m.%Y")
        self.month_1: datetime = datetime.strptime("01.10.2017", "%d.%m.%Y")

        self.start_dates: List(datetime) = [self.month_1, self.start_total, self.start_2017, self.month_6, self.month_3]

        self.data: Dict[str, Dict[str, CurrencyStatisticalData]] = dict()

        folder_today: str = str(datetime.now().year) + "-" + str(datetime.now().month) + "-" + str(datetime.now().day)
        path_today: str = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA, folder_today)
        GlobalData.EXTERNAL_PATH_ANALYSIS_DATA_TODAY = path_today
        if os.path.isdir(path_today):
            shutil.rmtree(path_today)
        os.mkdir(path_today)

        for start_date in self.start_dates:
            self.data[str(start_date)] = WithinCurrencies(start_date).get_and_export_data(
                self.currency_handler.get_all_currency_names())

            if start_date is None:
                start_date_name = "all-time"
            else:
                # continue
                start_date_name = str(start_date.timestamp())

            StatisticalAnalysisRunnerAndExporter(start_date_name, self.data[str(start_date)]).run()

            with_keyword, without_keyword = self.create_semantic_clusters()
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              with_keyword),
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              without_keyword),
                                                          subfolder="keyword-clustering").run()

            low_volume, high_volume = self.create_volume_clusters()
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(low_volume),
                                                          WithinCurrencies(start_date).get_and_export_data(high_volume),
                                                          subfolder="volume_clustering").run()

            low_start_price, high_start_price = self.create_start_price_clusters()
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              low_start_price),
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              high_start_price),
                                                          subfolder="start_price_clustering").run()

            coins, tokens = self.create_token_coin_clusters()
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              coins),
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              tokens),
                                                          subfolder="coin_token_clustering").run()

    def filter_for_keyword(self) -> Tuple[Dict, Dict]:
        contains_keyword = dict()
        no_keyword = dict()
        for start_date in self.data:
            data = self.data[start_date]
            for currency_statistical in data:
                if data[currency_statistical].currency.contains_keyword("any"):
                    contains_keyword[currency_statistical] = data[currency_statistical]
                else:
                    no_keyword[currency_statistical] = data[currency_statistical]

        return contains_keyword, no_keyword

    def get_keyword_data(self):
        standard_set = self.data["None"]
        index = list()
        figure_1 = list()
        for key in standard_set:
            currency = standard_set[key].currency
            item = (standard_set[key].first_date,
                    currency.contains_keyword("coin"),
                    currency.contains_keyword("token"),
                    currency.contains_keyword("bit"),
                    currency.contains_keyword("any"),
                    True)
            figure_1.append(item)
            index.append(standard_set[key].first_date)

        df = pandas.DataFrame(figure_1, index=index,
                              columns=["date", "coin", "token", "bit", "any", "all"]).sort_index()

        df["date"] = df["date"].astype("datetime64[ms]")
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).sum()
        df2["coin"] = df2["coin"] / df2["all"]
        df2["token"] = df2["token"] / df2["all"]
        df2["bit"] = df2["bit"] / df2["all"]
        df2["any"] = df2["any"] / df2["all"]
        del df2["all"]
        df2.plot(kind="bar")
        plt.show()

        return figure_1

    def get_start_time_analysis(self):
        standard_set = self.data["None"]
        index = list()
        output = list()

        for key in standard_set:
            index.append(standard_set[key].first_date)
            output.append(True)

        df = pandas.DataFrame(index, index=index, columns=["date"]).sort_index()
        fig, ax = plt.subplots()

        df["date"] = df["date"].astype("datetime64[ms]")
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).count()

        df2.plot(kind="bar", ax=ax, legend=False)
        index = list(df2.index)
        print(index)
        ax.set_xticklabels(index, rotation=90, fontsize=10)
        ax.set(xlabel="Time in months", ylabel="Frequency")
        fig.subplots_adjust(bottom=0.3)

        # fig.bottom = 0.55
        # fig.tight_layout()
        plt.show()

        return

    def create_semantic_clusters(self) -> Tuple[List[str], List[str]]:
        with_keyword = list()
        without_keyword = list()

        for currency in self.currency_handler.get_all_currency_names():
            if self.currency_handler.get_currency(currency).contains_keyword("any"):
                with_keyword.append(currency)
            else:
                without_keyword.append(currency)

        return with_keyword, without_keyword

    def create_volume_clusters(self) -> Tuple[List[str], List[str]]:
        currencies = self.currency_handler.get_all_currency_names()
        currencies = list(map(lambda x: self.currency_handler.get_currency(x), currencies))

        volume = list(map(lambda x: (x.currency, x.get_statistical_data().average_volume), currencies))
        volume = sorted(volume, key=lambda x: x[1])
        volume = list(map(lambda x: x[0], volume))

        middle = int(len(volume) / 2)

        return volume[:middle], volume[middle:]

    def create_start_price_clusters(self) -> Tuple[List[str], List[str]]:
        currencies = self.currency_handler.get_all_currency_names()
        currencies = list(map(lambda x: self.currency_handler.get_currency(x), currencies))

        start_prices = list(map(lambda x: (x.currency, x.get_statistical_data().first_price), currencies))
        start_prices = sorted(start_prices, key=lambda x: x[1])
        start_prices = list(map(lambda x: x[0], start_prices))

        middle = int(len(start_prices) / 2)

        return start_prices[:middle], start_prices[middle:]

    def create_token_coin_clusters(self) -> Tuple[List[str], List[str]]:
        tokens = self.coinmarketcap_tokens.get_all_tokens()
        tokens = list(map(lambda x: x["currency"], tokens))

        coins = self.coinmarketcap_coins.get_all_coins()

        return coins, tokens
