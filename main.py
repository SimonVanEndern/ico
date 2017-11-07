from datetime import datetime

import finance.analysis.descriptive_statistics as descriptives
from common.coinmarketCapApi import CoinmarketCapApi
from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser
from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency import Currency
from top.layer_on_top_of_within_currencies import LayerOnTopOfWithinCurrencies


class Main:
    coinmarketcap = CoinmarketCapApi(static=True)
    coinmarketcap_coins = CoinmarketCapCoinParser()
    coinmarketcap_tokens = CoinmarketCapTokenParser()
    descriptives = descriptives.DescriptiveStatistics()

    layer_on_top_of_within_currencies: LayerOnTopOfWithinCurrencies = None

    latest_only = False

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

            self.layer_on_top_of_within_currencies = LayerOnTopOfWithinCurrencies()

            # Figure02
            self.layer_on_top_of_within_currencies.get_start_time_analysis()

            # Includes keyword analysis
            keyword_data = descriptives.contains_keyword_coin(self.coinmarketcap.get_currencies())
            # Stat4: Total Cryptocurrencies investigated for keywords
            print("Total cryptocurrencies: " + str(keyword_data["total"]))
            # Stat5: Number of Cryptocurrencies containing the word token
            print("Contains 'token': " + str(keyword_data["token"]))
            # Stat6: Number of Cryptocurrencies containing the word coin
            print("Contains 'coin': " + str(keyword_data["coin"]))
            # Stat7: Number of Cryptocurrencies containing the word "bit"
            print("Contains 'bit': " + str(keyword_data["bit"]))

            # Figure03: Histogram of containing "coin"
            self.layer_on_top_of_within_currencies.get_keyword_data()

            # Figure04:
            self.descriptives.keyword_comparison_to_market_capitalilzation2()

            # Percentage of keyword "coin" for currencies without market capitalization
            stats = descriptives.contains_keyword_coin(self.coinmarketcap.get_market_cap_named(True))
            # Stat7
            print("CCs without available market cap: " + str(stats["total"]))
            # Stat8
            print("Percentage containing 'coin' of ccs without market cap: " + str(stats["coin"] / stats["total"]))

        # Figure05:
        # Average volume plot
        self.layer_on_top_of_within_currencies.get_average_volume_data()

        # Figure06:
        # Average market capitalization plot
        self.layer_on_top_of_within_currencies.get_average_market_capitalization_plot()

        # Stat8
        # Correlation between average volume and average market capitalization
        self.layer_on_top_of_within_currencies.get_correlation_between_average_volume_and_average_market_capitalization()

        # Figure 07:
        # Average market capitalization divided by average volume
        # Stat9
        # Average average of this
        self.layer_on_top_of_within_currencies.get_average_market_capitalization_divided_by_average_volume_plot()

        # Table1: Showing the correlation of volume and usd with increasing correlation
        bitcoin = Currency("ripple", date_limit=datetime.strptime("01.11.2016", "%d.%m.%Y"))
        # bitcoin.print_volume_return_correlations()

        # Correlation volume and price
        # Stat9
        # aggregator = Aggregator()
        # print(aggregator.get_volume_price_correlation())
        # for key, value in (aggregator.get_volume_price_aggregation_2()).items():
        #     print(key)
        #     print(value)


run_script = Main()
