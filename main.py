from common.aggregated import Aggregator
from common.coinmarketCapApi import CoinmarketCapApi
from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser
from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency import Currency
from finance.analysis.descriptive_statistics import DescriptiveStatistics
import finance.analysis.descriptive_statistics as descriptives


class Main:
    coinmarketcap = CoinmarketCapApi()
    coinmarketcap_coins = CoinmarketCapCoinParser()
    coinmarketcap_tokens = CoinmarketCapTokenParser()
    descriptives = DescriptiveStatistics()

    latest_only = True

    def __init__(self):
        if not self.latest_only:
            # Stat1: Amount of currencies listed on Coinmarketcap
            print("Total Currencies: " + str(len(self.coinmarketcap.get_all_currencies())))

            # Stat2: Amount of coins listed on Coinmarketcap
            print("Coins: " + str(len(self.coinmarketcap_coins.get_all_coins())))

            # Stat3: Amount of tokens listed on Coinmarketcap
            print("Tokens: " + str(len(self.coinmarketcap_tokens.get_all_tokens())))

            # Figure01
            # Stat4: Number of platforms for tokens listed on coinmarketcap
            print("Platforms: " + str(self.coinmarketcap_tokens.get_platform_statistics()))

            # Figure02
            self.descriptives.start_time_data_analysis()

            # Includes keyword analysis
            keyword_data = descriptives.contains_keyword_coin(self.coinmarketcap.get_currencies())
            # Stat4: Total Cryptocurrencies investigated for keywords
            print("Total cryptocurrencies: " + str(keyword_data["total"]))
            # Stat5: Number of Cryptocurrencies containing the word token
            print("Contains 'token': " + str(keyword_data["token"]))
            # Stat6: Number of Cryptocurrencies containing the word coin
            print("Contains 'coin': " + str(keyword_data["coin"]))

            # Figure03: Histogram of containing "coin"
            self.descriptives.start_time_data_analysis_including_keyword()

            # Figure04:
            self.descriptives.keyword_comparison_to_market_capitalilzation2()

            # Percentage of keyword "coin" for currencies without market capitalization
            stats = descriptives.contains_keyword_coin(self.coinmarketcap.get_market_cap_named(True))
            # Stat7
            print("CCs without available market cap: " + str(stats["total"]))
            # Stat8
            print("Percentage containing 'coin' of ccs without market cap: " + str(stats["coin"] / stats["total"]))

        # Table1: Showing the correlation of volume and usd with increasing correlation
        bitcoin = Currency("ripple", date_limit="01.11.2016")
        bitcoin.print_volume_return_correlations()

        # Correlation volume and price
        # Stat9
        aggregator = Aggregator()
        # print(aggregator.get_volume_price_correlation())
        for key, value in (aggregator.get_volume_price_aggregation_2()).items():
            print(key)
            print(value)


run_script = Main()
