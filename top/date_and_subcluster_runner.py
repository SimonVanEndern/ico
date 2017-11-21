import os
import shutil
from datetime import datetime
from typing import List, Dict, Tuple

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

        self.start_dates: List(datetime) = [self.start_total, self.start_2017, self.month_6, self.month_3, self.month_1]

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

            low_start_date, high_start_date = self.create_property_cluster("start_date")
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              low_start_date),
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              high_start_date),
                                                          subfolder="start_date_clustering").run()
            low_market_cap, high_market_cap = self.create_property_cluster("average_market_capitalization")
            ClusteredStatisticalAnalysisRunnerAndExporter(start_date_name,
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              low_market_cap),
                                                          WithinCurrencies(start_date).get_and_export_data(
                                                              high_market_cap),
                                                          subfolder="market_cap_clustering").run()

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

    def create_property_cluster(self, property_name: str) -> Tuple[List[str], List[str]]:
        currencies = self.currency_handler.get_all_currency_names()
        currencies = list(map(lambda x: self.currency_handler.get_currency(x), currencies))

        property_list = list(map(lambda x: (x.currency, getattr(x.get_statistical_data(), property_name)), currencies))
        property_list = sorted(property_list, key=lambda x: x[1])
        property_list = list(map(lambda x: x[0], property_list))

        middle = int(len(property_list) / 2)

        return property_list[:middle], property_list[middle:]

    def create_cluster_significant_volume_price_correlation(self) -> Tuple[List[str], List[str]]:
        currencies = self.currency_handler.get_all_currency_names()
        currencies = list(map(lambda x: self.currency_handler.get_currency(x), currencies))

        correlations = list(map(lambda x: (x.currency, x.get_statistical_data().volume_price_correlations["0"]), currencies))
        correlations = sorted(correlations, key=lambda x: x[1][1])
        correlations_significant = list(filter(lambda x: x[1][1] < 0.1, correlations))
        correlations_significant = list(map(lambda x: x[0], correlations_significant))
        correlations_not_significant = list(filter(lambda x: x[1][1] >= 0.1, correlations))
        correlations_not_significant = list(map(lambda x: x[0], correlations_not_significant))

        return correlations_significant, correlations_not_significant
