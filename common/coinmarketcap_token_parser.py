from collections import Counter
from datetime import datetime
from os import path

import matplotlib.pyplot as plt
import pandas
from bs4 import BeautifulSoup

from common.currency_handler import CurrencyHandler
from common.parser import Parser


class CoinmarketCapTokenParser(Parser):
    currency_handler: CurrencyHandler = CurrencyHandler.Instance()
    import_address = "https://coinmarketcap.com/tokens/views/all/"
    now = datetime.now()
    path_to_save = path.join(path.dirname(__file__) + "\saved",
                             "coinmarketcap-tokens" + str(now.year) + str(now.month) + str(now.day) + ".html")

    def __init__(self, static=False):
        super().__init__()

        if static:
            self.path_to_save = path.join(path.dirname(__file__) + "\saved", "coinmarketcap-tokens2017112.html")

    def get_all_tokens(self):
        output: list = list()
        with open(self.path_to_save, "r", encoding="utf8") as file:
            soup = BeautifulSoup(file, "html.parser")
            table = soup.find("table", {"id": "assets-all"})
            rows = table.find_all("tr")
            for index, row in enumerate(rows):
                # Skip headers
                if index == 0:
                    continue
                currency_href = row.find("td", {"class": "currency-name"}).find("a")['href']
                splits = currency_href.split("/")
                currency_name = splits[len(splits) - 2]
                platform_name = row.find("td", {"class": "platform-name"}).find("a").text
                output.append({"currency": currency_name, "platform": platform_name})

        all_currencies = self.currency_handler.get_all_currency_names()
        to_remove = list()
        for currency in output:
            if currency["currency"] not in all_currencies:
                to_remove.append(currency)

        for currency in to_remove:
            output.remove(currency)

        return output

    def get_platform_statistics(self):
        tokens = self.get_all_tokens()
        tokens = list(map(lambda x: x["platform"], tokens))

        token_counts = Counter(tokens)
        token_counts["Ethereum Cl."] = token_counts["Ethereum Classic"]
        token_counts.pop("Ethereum Classic")

        fig, ax = plt.subplots(2, 1, sharex="all")
        ax[1].set_ylim(0, 30)
        ax[0].set_ylim(230, 250)

        ax[0].spines['bottom'].set_visible(False)
        ax[1].spines['top'].set_visible(False)

        ax[0].xaxis.tick_top()
        ax[0].tick_params(labeltop='off')  # don't put tick labels at the top
        ax[1].xaxis.tick_bottom()

        d = .015  # how big to make the diagonal lines in axes coordinates
        # arguments to pass to plot, just so we don't keep repeating them
        kwargs = dict(transform=ax[0].transAxes, color='k', clip_on=False)
        ax[0].plot((-d, +d), (-d, +d), **kwargs)        # top-left diagonal
        ax[0].plot((1 - d, 1 + d), (-d, +d), **kwargs)  # top-right diagonal

        kwargs.update(transform=ax[1].transAxes)  # switch to the bottom axes
        ax[1].plot((-d, +d), (1 - d, 1 + d), **kwargs)  # bottom-left diagonal
        ax[1].plot((1 - d, 1 + d), (1 - d, 1 + d), **kwargs)  # bottom-right diagonal

        fig.suptitle("Distribution of crypto-currencies according to used blockchain",
                     fontsize=10)
        df = pandas.DataFrame.from_dict(token_counts, orient='index')

        print(df)
        df.plot(kind='bar', ax=ax[0], legend=False)
        df.plot(kind='bar', ax=ax[1], legend=False)
        ax[1].set_xticklabels(df.index, rotation=90, fontsize=10)
        ax[1].set(xlabel="Used crypto-currency", ylabel="Absolute count")
        # fig.bottom = 0.55
        # fig.tight_layout()
        fig.subplots_adjust(top=0.9, bottom=0.3)
        # fig.set_size_inches(18.5, 10.5)



        plt.show()

        return len(token_counts)

# run_script = CoinmarketCapTokenParser()
# run_script.get_platform_statistics()
