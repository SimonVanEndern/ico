from datetime import datetime
from typing import List, Dict

from common.currency_statistical_data import CurrencyStatisticalData
from top.within_currencies import WithinCurrencies


class LayerOnTopOfWithinCurrencies:
    def __init__(self):
        # Using data for whole period
        self.start_total = None

        # Using data from begin 2017 on
        self.start_2017: datetime = datetime.strptime("01.01.2017", "%d.%m.%Y")

        # Using data of last 6 month
        self.month_6: datetime = datetime.strptime("01.05.2017", "%d.%m.%Y")

        # Using data of last 3 month
        self.month_3: datetime = datetime.strptime("01.08.2017", "%d.%m.%Y")

        self.start_dates: List(datetime) = [self.start_total, self.start_2017, self.month_6, self.month_3]

        self.data: Dict[str, Dict[str, CurrencyStatisticalData]] = dict()

        for start_date in self.start_dates:
            self.data[str(start_date)] = WithinCurrencies(start_date).get_and_export_data()

            # Clustering according to "coin" semantics
            self.data_semantic_cluster: Dict = dict()
            self.data_semantic_cluster["contains_keyword"], self.data_semantic_cluster[
                "no_keyword"] = self.filter_for_keyword()
            # Clustering according to available funding data
            # Clustering according to volume

    def filter_for_keyword(self):
        contains_keyword = dict()
        no_keyword = dict()
        for start_date in self.data:
            data = self.data[start_date]
            for currency_statistical in data:
                if data[currency_statistical].currency.contains_keyword():
                    contains_keyword[currency_statistical] = data[currency_statistical]
                else:
                    no_keyword[currency_statistical] = data[currency_statistical]

        return contains_keyword, no_keyword


LayerOnTopOfWithinCurrencies()
