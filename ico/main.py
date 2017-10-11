from common.coinmarketCapApi import CoinmarketCapApi
from ico.sources.blockstarter import BlockstarterSource
from ico.sources.coindesk import CoindeskSource
from ico.sources.coinschedule import CoinscheduleSource
from ico.sources.cyberfund import CyberfundSource
from ico.sources.icobazaar import IcobazaarSource
from ico.sources.icotracker import IcotrackerSource
from ico.sources.smithandcrown import SmithandcrownSource


class Main:
    data = {}

    def __init__(self):
        self.coinmarketcap_source = CoinmarketCapApi()
        self.coindesk_source = CoindeskSource()
        self.icobazaar_source = IcobazaarSource()
        self.icotracker_source = IcotrackerSource()
        self.coinschedule_source = CoinscheduleSource()
        self.smithandcrown_source = SmithandcrownSource()
        self.cyberfund_source = CyberfundSource()
        self.blockstarter_source = BlockstarterSource()

        self.currency_map = self.coinmarketcap_source.getShortnameMap()

        self.getData()

    def add_data(self, newData):
        for key in newData:
            if key in self.data:
                self.data[key].addData(newData[key].raised_money)
                if newData[key].close_date is not None:
                    self.data[key].close_date = newData[key].close_date
            else:
                self.data[key] = newData[key]

    def getData(self):
        coindesk_data = self.coindesk_source.getIcoData(self.currency_map)
        icobazaar_data = self.icobazaar_source.getIcoData(self.currency_map)
        icotracker_data = self.icotracker_source.getIcoData(self.currency_map)
        coinschedule_data = self.coinschedule_source.getIcoData(self.currency_map)
        coinmarketcap_data = self.coinmarketcap_source.getIcoData()
        smithandcrown_data = self.smithandcrown_source.getIcoData(self.currency_map)
        cyberfund_data = self.cyberfund_source.getIcoData(self.currency_map)
        blockstarter_data = self.blockstarter_source.getIcoData(self.currency_map)

        self.add_data(coindesk_data)
        self.add_data(icobazaar_data)
        self.add_data(icotracker_data)
        self.add_data(coinschedule_data)
        self.add_data(coinmarketcap_data)
        self.add_data(smithandcrown_data)
        self.add_data(cyberfund_data)
        self.add_data(blockstarter_data)

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


# run_script = Main()
# run_script.log_data()
# run_script.log_important_statistics()
# run_script.log_ordered_by_date()
