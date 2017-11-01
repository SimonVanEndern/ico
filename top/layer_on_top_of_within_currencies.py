from datetime import datetime
from typing import List

from top.within_currencies import WithinCurrencies


class LayerOnTopOfWithinCurrencies:
    def __init__(self):
        # Using data for whole period
        # Using data from begin 2017 on
        # Using data of last 6 month
        # Using data of last 3 month
        self.start_2017: datetime = datetime.strptime("01.01.2017", "%d.%m.%Y")
        self.month_6: datetime = datetime.strptime("01.05.2017", "%d.%m.%Y")
        self.month_3: datetime = datetime.strptime("01.08.2017", "%d.%m.%Y")

        self.start_dates: List(datetime) = [None, self.start_2017, self.month_6, self.month_3]

        self.data: dict = dict()

        for start_date in self.start_dates:
            self.data[start_date] = WithinCurrencies(start_date).get_data()

        # Clustering according to "coin" semantics
        # Clustering according to available funding data
        # Clustering according
