import os.path
from datetime import datetime

import matplotlib.pyplot as plt
import pandas

import common.coinmarketCapApi
import common.currency
from finance.analysis.coinmarket_start_time import AggregateCoinmarketStartTimeAndAverageVolume


def contains_keyword_coin(currencies):
    contain_coin = 0
    contain_token = 0

    for currency in currencies:
        if currency.find("coin") != -1:
            contain_coin += 1
        if currency.find("token") != -1:
            contain_token += 1

    return {"total": len(currencies), "coin": contain_coin, "token": contain_token}


class DescriptiveStatistics:
    example_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-09-28"
    coinmarketcap = common.coinmarketCapApi.CoinmarketCapApi()

    # Change away from static bitcoin
    currency_provider = common.currency.Currency("bitcoin")

    now = datetime.now()
    path = os.path.join(os.path.dirname(__file__) + "\\aggregated",
                        "start_date" + str(now.year) + str(now.month) + str(now.day) + ".csv")

    def __init__(self):
        AggregateCoinmarketStartTimeAndAverageVolume(self.coinmarketcap)
        return

    # Printing a histogram of the number of currencies started to be listed at coinmarketcap by month
    def start_time_data_analysis(self):
        df = pandas.read_csv(self.path)
        del df["Currency"]
        df["Start-Date"] = df["Start-Date"].astype("datetime64[ns]")
        df.groupby([df["Start-Date"].dt.year, df["Start-Date"].dt.month]).count().plot(kind="bar")
        print("Figure 02: ")
        plt.show()

        return

    def start_time_data_analysis_including_keyword(self):
        df = pandas.read_csv(self.path)
        df["Includes_Coin"] = df.apply(lambda row: row["Currency"].find("coin") != -1, axis=1)
        df["Not_Includes_Coin"] = df.apply(lambda row: row["Currency"].find("coin") == -1, axis=1)
        del df["Currency"]
        df["Start-Date"] = df["Start-Date"].astype("datetime64[ns]")
        df.groupby([df["Start-Date"].dt.year, df["Start-Date"].dt.month]).sum().plot(kind="bar")
        print("Figure 03: ")
        plt.show()

        return

    def get_market_capitalization_histogram(self):
        market_cap = self.coinmarketcap.get_market_cap_named()
        # market_cap.pop("bitcoin")
        # market_cap.pop("ethereum")
        df = pandas.DataFrame.from_dict(market_cap, orient='index')
        print(df)
        # bins = numpy.linspace(math.ceil(min(market_cap)),
        #                    math.floor(max(market_cap)),
        #                    20)
        bins = [0, 100, 1000, 10000, 100000, 1000000, 10000000, 100000000, 1000000000]
        # df.groupby('').count().plot(kind="bar")
        plt.hist(df, bins)
        # plt.hist(market_cap, bins='auto', normed=True)
        # plt.boxplot(df)
        # df.boxplot()
        plt.show()

    def get_highest_lowest_market_cap(self):
        currencies = self.coinmarketcap.get_currencies()
        ouput = []
        for index, currency in enumerate(currencies):
            if index == 3:
                break
            data = self.currency_provider.get_volume_financial_data(currency)
            sorted_data = sorted(data, key=lambda x: x[1], reverse=True)
            highest = sorted_data[0]
            print(highest)

    # Deprecated
    def keyword_comparison_to_market_capitalilzation(self):
        currencies = self.coinmarketcap.get_market_cap_named()
        currency_list = list(dict.items(currencies))
        # for key, value in currencies.iteritems():
        #     currency_list.append((key, currencies[key]))
        currency_list.sort(key=lambda x: x[1], reverse=True)
        bucket_size = 100
        output = []
        bucket = 0
        count = 0
        keyword_count = 0
        for currency in currency_list:
            if count == bucket_size:
                output.append((bucket, keyword_count / bucket_size, (bucket_size - keyword_count) / bucket_size))
                count = 0
                bucket += 1
                keyword_count = 0

            if currency[0].find("coin") != -1:
                keyword_count += 1

            count += 1
        output.append((bucket, keyword_count / count, (count - keyword_count) / count))

        df = pandas.DataFrame(output)
        del df[0]
        chart = df.plot()
        chart.legend(["Contains_coin", "No_keyword"])

        # Figure04
        plt.show()

        return output

    def keyword_comparison_to_market_capitalilzation2(self):
        currencies = self.coinmarketcap.get_market_cap_named()
        currency_list = list(dict.items(currencies))
        currency_list.sort(key=lambda x: x[1], reverse=True)
        bucket_size = 50
        output = []
        keyword_counter = []
        for index, currency in enumerate(currency_list):
            if currency[0].find("coin") != -1:
                keyword_counter.append(1)
            else:
                keyword_counter.append(0)

            if index >= bucket_size:
                keyword_counter.pop(0)
                output.append(sum(keyword_counter) / bucket_size)

        df = pandas.DataFrame(output)
        chart = df.plot()

        # Figure04
        plt.show()

        return output

# run_script = DescriptiveStatistics()
# run_script.keyword_comparison_to_market_capitalilzation2()
