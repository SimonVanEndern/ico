import csv
import os
from datetime import datetime
from typing import Dict

from common.currency import Currency
from common.currency_handler import CurrencyHandler
from common.currency_statistical_data import CurrencyStatisticalData
from global_data import GlobalData


class WithinCurrencies:
    def __init__(self, start_date: datetime = None):
        self.start_date: datetime = start_date
        self.currency_handler: CurrencyHandler = CurrencyHandler()
        self.data: Dict[str, CurrencyStatisticalData] = dict()
        self.filename: str = "within-currencies-analysis" + str(datetime.now().timestamp() * 1e3) + ".csv"
        self.save_path: str = os.path.join(GlobalData.EXTERNAL_PATH_ANALYSIS_DATA, self.filename)

    def get_and_export_data(self):
        file = open(self.save_path)
        writer = csv.writer(file)

        for currency in self.currency_handler.get_all_currency_names():
            handle_on_currency: Currency = self.currency_handler.get_currency(currency, date_limit=self.start_date)
            self.data[currency] = handle_on_currency.get_statistical_data()
            # writer.writerow(self.data[currency].to_csv())
            print(currency)
            print(self.data[currency].to_json_export())

        file.close()
        return self.data


WithinCurrencies().get_and_export_data()
