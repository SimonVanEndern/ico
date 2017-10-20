import json
import logging
import os.path
import time

import requests

from common.currency_handler import CurrencyHandler
from csv_strings import CSVStrings
from global_data import GlobalData


# logging.basicConfig(level=logging.DEBUG)


def check_data_already_downloaded(currency, start, end, save_path):
    filename = str(start) + "-" + str(end) + ".json"
    return os.path.isfile(os.path.join(save_path, currency, filename))


class CoinMarketCapGraphAPIImporter:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.price_usd_string = CSVStrings.price_usd_string

        self.raw_data_path = GlobalData.EXTERNAL_PATH_RAW_DATA
        self.save_path_additional_data = GlobalData.EXTERNAL_PATH_ADDITIONAL_DATA

        self.currency_handler = CurrencyHandler()

    def request_currency(self, currency, last_date):
        if os.path.isfile(os.path.join(self.raw_data_path, currency, "ready" + str(last_date))):
            self.logger.info("All currencies until {} already downloaded".format(last_date))
            return

        first_date = self.currency_handler.get_basic_currency_data(currency)["start_date"]

        # Requesting data before data for this currency was available
        if last_date < first_date:
            return

        if not os.path.isdir(os.path.join(self.raw_data_path, currency)):
            os.mkdir(os.path.join(self.raw_data_path, currency))

        self.request_data_monthly(currency, first_date, last_date)

        # Mark currency as completely downloaded for this "last_date" time
        open(os.path.join(self.raw_data_path, currency, "ready" + str(last_date)), "w").close()

    def request_data_monthly(self, currency, first_date, last_date):
        span_month = 29 * 24 * 60 * 60 * 1000

        start = first_date
        while start + span_month < last_date:
            data = self.request_data(currency, start, start + span_month, self.raw_data_path)
            self.save_data(data, currency, start, start + span_month, self.raw_data_path)

            start += span_month

        data = self.request_data(currency, start, last_date, self.raw_data_path)
        self.save_data(data, currency, start, last_date, self.raw_data_path)

    def request_data(self, currency, start, end, save_path):
        if check_data_already_downloaded(currency, start, end, save_path):
            return None

        print("Sleeping for 1 secs")
        time.sleep(1)

        path = ("https://" +
                GlobalData.coin_market_cap_graph_api_url +
                "/currencies/{}/{}/{}/".format(currency, start, end))
        response = requests.request("GET", path)
        print("Path: " + path)

        try:
            data = json.loads(response.text)
        except json.decoder.JSONDecodeError:
            data = None
            self.logger.warning("No results: {}".format(path))

        return data

    def save_data(self, data, currency, start, end, path):
        if data is None:
            self.logger.info("Currency {} from {} to {} already downloaded".format(currency, start, end))
            return

        if len(data[self.price_usd_string]) == 2:
            self.logger.info("Currency {} from {} to {} has no additional data".format(currency, start, end))
            # return

        self.logger.info("saved data from {} to {} --> {} entries".format(start, end, len(data[self.price_usd_string])))
        if len(data[self.price_usd_string]) < 800:
            self.logger.warning(
                "For {} to {} we only got {} entries".format(start, end, len(data[self.price_usd_string])))

        filename = str(start) + "-" + str(end) + ".json"
        if not os.path.isdir(os.path.join(path, currency)):
            os.mkdir(os.path.join(path, currency))

        with open(os.path.join(path, currency, filename), "w") as file:
            json.dump(data, file)

    def request_additional_data(self, currency, time_span_tuples):
        for time_span in time_span_tuples:
            data = self.request_data(currency, time_span[0], time_span[1], self.save_path_additional_data)
            self.save_data(data, currency, time_span[0], time_span[1], self.save_path_additional_data)

        if os.path.isdir(os.path.join(self.save_path_additional_data, currency)):
            open(os.path.join(self.save_path_additional_data, currency,
                              "ready" + str(GlobalData.last_date_for_download)), "w").close()
