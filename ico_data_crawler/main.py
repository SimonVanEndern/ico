import json
import logging
from datetime import datetime

import os

from common.coinmarketCapApi import CoinmarketCapApi
from common.main.json_converter import JsonConverter
from global_data import GlobalData
from ico_data_crawler.imports.blockstarter import BlockstarterSource
from ico_data_crawler.imports.coindesk import CoindeskSource
from ico_data_crawler.imports.coinschedule import CoinscheduleSource
from ico_data_crawler.imports.cyberfund import CyberfundSource
from ico_data_crawler.imports.icobazaar import IcobazaarSource
from ico_data_crawler.imports.icotracker import IcotrackerSource
from ico_data_crawler.imports.smithandcrown import SmithandcrownSource
from ico_data_crawler.matcher import CurrencyNameMatcher

logging.basicConfig(level=logging.INFO)


class Main:
    data = {}

    def __init__(self):
        logging.info("Constructing ico:Main")

        self.coinmarketcap_source = CoinmarketCapApi()
        self.coindesk_source = CoindeskSource()
        self.icobazaar_source = IcobazaarSource()
        self.icotracker_source = IcotrackerSource()
        self.coinschedule_source = CoinscheduleSource()
        self.smithandcrown_source = SmithandcrownSource()
        self.cyberfund_source = CyberfundSource()
        self.blockstarter_source = BlockstarterSource()

        self.currency_map = self.coinmarketcap_source.getShortnameMap()

        self.currency_matcher = CurrencyNameMatcher()

        self.collect_data()

        logging.info("Finished constructing ico:Main")

    def collect_data(self):
        coindesk_data = self.coindesk_source.get_ico_data()
        icobazaar_data = self.icobazaar_source.getIcoData()
        icotracker_data = self.icotracker_source.getIcoData()
        coinschedule_data = self.coinschedule_source.getIcoData()
        coinmarketcap_data = self.coinmarketcap_source.getIcoData()
        smithandcrown_data = self.smithandcrown_source.getIcoData()
        cyberfund_data = self.cyberfund_source.getIcoData()
        blockstarter_data = self.blockstarter_source.getIcoData()

        sources = [coindesk_data, icobazaar_data, icotracker_data, coinschedule_data, coinmarketcap_data,
                   smithandcrown_data, cyberfund_data, blockstarter_data]

        for source in sources:
            self.add_data(self.currency_matcher.match(source))

    def add_data(self, newData):
        for key in newData:
            if key in self.data:
                self.data[key].addData(newData[key].raised_money)
                if newData[key].close_date is not None:
                    self.data[key].close_date = newData[key].close_date
            else:
                self.data[key] = newData[key]

    def get_data(self):
        return self.currency_matcher.unmatch_symbol(self.data)

    def log_data(self):
        count_funding_data = 0
        count_date_data = 0
        for key in sorted(self.data):
            if self.data[key].funds:
                count_funding_data += 1
            if self.data[key].close_date is not None:
                count_date_data += 1
            print(key + ": " + str(self.data[key]))

        print("Funding " + str(count_funding_data))
        print("Date " + str(count_date_data))
        print(len(self.data))

    def log_important_statistics(self):
        print("Coinmarketcap currencies / projects:")
        count = 0
        for currency in self.coinmarketcap_source.get_currencies(multiple=True):
            if currency[0] in self.data:
                if self.data[currency[0]].funds:
                    count += 1
                    continue
            if currency[1] in self.data:
                if self.data[currency[1]].funds:
                    count += 1
                    continue

            print(currency)

        print(count)

        return

    def log_ordered_by_date(self):
        # for currency in sorted(self.data.values(), key=lambda operator.attrgetter("close_date"): float('inf') if ):
        #     print(currency)
        listing = []
        for currency in self.data:
            listing.append(self.data[currency])
            if self.data[currency] is None:
                print(currency)

        for currency in sorted(listing):
            print(currency)
            # for currency in self.data:
            #     print(type(currency))
            #     print(type(self.data[currency]))

    # def save_data(self):
    #     filename = "ico-data" + str(datetime.now().strftime("%Y-%m-%d")) + ".json"
    #     filepath = os.path.join(GlobalData.ICO_FUNDING_AND_START_DATA_PATH, filename)
    #     data = self.get_data()
    #     print(data)
    #
    #     if os.path.isfile(filepath):
    #         os.remove(filepath)
    #
    #     with open(filepath, "w") as file:
    #         json.dump(data, file, cls=JsonConverter)


# run_script = Main()
# run_script.save_data()
# run_script.log_data()
# run_script.log_important_statistics()
# run_script.log_ordered_by_date()
