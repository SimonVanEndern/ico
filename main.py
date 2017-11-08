import os
from datetime import datetime
from pprint import pprint

import finance.analysis.descriptive_statistics as descriptives
from common.coinmarketCapApi import CoinmarketCapApi
from common.coinmarketcap_coin_parser import CoinmarketCapCoinParser
from common.coinmarketcap_token_parser import CoinmarketCapTokenParser
from common.currency import Currency
from global_data import GlobalData
from top.layer_on_top_of_within_currencies import LayerOnTopOfWithinCurrencies


class Main:
    coinmarketcap = CoinmarketCapApi(static=True)
    coinmarketcap_coins = CoinmarketCapCoinParser()
    coinmarketcap_tokens = CoinmarketCapTokenParser()
    descriptives = descriptives.DescriptiveStatistics()

    layer_on_top_of_within_currencies = LayerOnTopOfWithinCurrencies()

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

        frame_name = "all-currencies"
        save_path = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA, frame_name)
        if not os.path.isdir(save_path):
            os.mkdir(save_path)

        data = list()

        # Figure05:
        # Average volume plot
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_volume_data()
        fig.savefig(os.path.join(save_path, "Figure05-" + fig_name + ".png"))

        # Figure06:
        # Average market capitalization plot
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_market_capitalization_plot()
        fig.savefig(os.path.join(save_path, "Figure06-" + fig_name + ".png"))

        # Stat8
        # Correlation between average volume and average market capitalization
        correlation = self.layer_on_top_of_within_currencies.get_correlation_between_average_volume_and_average_market_capitalization()
        data.append((frame_name,
                     "Correlation Average Volume and Average Market Capitalization",
                     "coefficient: " + str(correlation[0]),
                     "p-value: " + str(correlation[1])))

        # Figure 07:
        # Average market capitalization divided by average volume
        fig, fig_name = self.layer_on_top_of_within_currencies.get_average_market_capitalization_divided_by_average_volume_plot()
        fig.savefig(os.path.join(save_path, "Figure07-" + fig_name + ".png"))

        # Stat9
        # Average average of this
        mean, median = self.layer_on_top_of_within_currencies.get_average_market_capitalization_divided_by_average_volume()
        data.append((frame_name,
                     "Average of average market capitalization divided by average volume",
                     "mean: " + str(mean),
                     "median: " + str(median)))

        # Figure 08:
        # Correlation of price and volume change
        fig, fig2, fig_name, fig_name2 = self.layer_on_top_of_within_currencies.get_volume_return_correlation_plot()
        fig.canvas.set_window_title("Figure XX")
        fig.savefig(os.path.join(save_path, "Figure08-" + fig_name + ".png"))
        fig2.savefig(os.path.join(save_path, "Figure09-" + fig_name2 + ".png"))

        # Stat 10:
        # Descriptive statistics of price and volume change
        des1, des2 = self.layer_on_top_of_within_currencies.get_volume_return_correlation_data()
        data.append((frame_name,
                     "Mean of correlation volume and return all",
                     "mean: " + str(des1["mean"]),
                     "count: " + str(des1["count"])))
        data.append((frame_name,
                     "Mean of correlation volume and return only significant ones",
                     "mean: " + str(des2["mean"]),
                     "count: " + str(des2["count"])))

        pprint(data)

        # Figure 09:
        # Correlation of price and volume change predictor search
        self.layer_on_top_of_within_currencies.get_volume_price_correlation_cause_search_plot()

        # Stat 10
        # Correlation between age and average market capitalization
        # Stat 11
        # Correlation between age and last market capitalization
        self.layer_on_top_of_within_currencies.print_age_market_capitalization_correlations()

        # Stat 11
        # Correlation between age and average volume
        self.layer_on_top_of_within_currencies.print_age_average_volume_correlation()

        # Figure 10:
        # Slope of linear regression on price
        self.layer_on_top_of_within_currencies.get_linear_price_regressions_plot()

        # TODO:
        self.layer_on_top_of_within_currencies.get_absolute_volume_price_correlation_plot()

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
