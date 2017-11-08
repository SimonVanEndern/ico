from datetime import datetime
from typing import List, Dict, Tuple

import matplotlib.pyplot as plt
import pandas

from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from top.statistical_analysis_runner_and_exporter import StatisticalAnalysisRunnerAndExporter
from top.within_currencies import WithinCurrencies


class LayerOnTopOfWithinCurrencies:
    def __init__(self):
        # Using data for whole period
        self.start_total: datetime = None

        # Using data from begin 2017 on
        self.start_2017: datetime = datetime.strptime("01.01.2017", "%d.%m.%Y")

        # Using data of last 6 month
        self.month_6: datetime = datetime.strptime("01.05.2017", "%d.%m.%Y")

        # Using data of last 3 month
        self.month_3: datetime = datetime.strptime("01.08.2017", "%d.%m.%Y")

        self.start_dates: List(datetime) = [self.start_total, self.start_2017, self.month_6, self.month_3]

        self.data: Dict[str, Dict[str, CurrencyStatisticalData]] = dict()

        for start_date in self.start_dates:
            if start_date is not None:
                break
            self.data[str(start_date)] = WithinCurrencies(start_date).get_and_export_data()

            # Clustering according to "coin" semantics
            self.data_semantic_cluster: Dict = dict()
            self.data_semantic_cluster["contains_keyword"], self.data_semantic_cluster[
                "no_keyword"] = self.filter_for_keyword()
            # Clustering according to available funding data
            # Clustering according to volume

        self.currency_handler = CurrencyHandler(static=True)

        StatisticalAnalysisRunnerAndExporter("all-currencies", self.data["None"]).run()

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

        df["date"] = df["date"].astype("datetime64[ms]")
        print(df)
        df2 = df.groupby([df["date"].dt.year, df["date"].dt.month]).count()
        print(df2)

        df2.plot(kind="bar")
        plt.show()

        return
