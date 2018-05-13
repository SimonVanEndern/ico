import json
import logging
import os.path
import time

import requests

from common.currency_handler import CurrencyHandler
from csv_strings import CSVStrings
from global_data import GlobalData


def check_data_already_downloaded(currency, start, end, save_path):
    filename = str(start) + "-" + str(end) + ".json"
    return os.path.isfile(os.path.join(save_path, currency, filename))


class CoinMarketCapGraphAPIImporter:
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)

        self.raw_data_path = GlobalData.EXTERNAL_PATH_RAW_DATA
        if not os.path.isdir(self.raw_data_path):
            os.mkdir(self.raw_data_path)

        self.save_path_additional_data = GlobalData.EXTERNAL_PATH_ADDITIONAL_DATA

        self.currency_handler = CurrencyHandler.Instance()

    def request_currency(self, currency, last_date):
        if currency == "bonpay":
            x=7
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

        dates = list(range(first_date, last_date, span_month))
        dates = list(map(lambda x: [x, x + span_month], dates))
        dates[len(dates) - 1][1] = last_date

        for date_tuple in dates:
            data = self.request_data(currency, date_tuple[0], date_tuple[1], self.raw_data_path)
            self.save_data(data, currency, date_tuple[0], date_tuple[1], self.raw_data_path)

    def request_data(self, currency, start, end, save_path):
        if check_data_already_downloaded(currency, start, end, save_path):
            return None

        print("Sleeping for 1 secs")
        time.sleep(1)

        path = (
            "https://" + GlobalData.COIN_MARKET_CAP_GRAPH_API_URL + "/currencies/{}/{}/{}/".format(currency, start,
                                                                                                   end))
        self.logger.info("Start: Downloading from " + path)
        response = requests.request("GET", path)
        self.logger.info("End: Downloading from " + path)

        if response.status_code != 200:
            self.logger.warning("No results: {}".format(path))
        else:
            return json.loads(response.text)

    def save_data(self, data, currency, start, end, path):
        if data is None:
            self.logger.info("Currency {} from {} to {} already downloaded".format(currency, start, end))
            return

        if len(data[CSVStrings.PRICE_USD_STRING]) == 2:
            self.logger.info("Currency {} from {} to {} has no additional data".format(currency, start, end))

        self.logger.info(
            "saved data from {} to {} --> {} entries".format(start, end, len(data[CSVStrings.PRICE_USD_STRING])))
        if len(data[CSVStrings.PRICE_USD_STRING]) < 800:
            self.logger.warning(
                "For {} to {} we only got {} entries".format(start, end, len(data[CSVStrings.PRICE_USD_STRING])))

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
                              "ready" + str(GlobalData.LAST_DATA_FOR_DOWNLOAD)), "w").close()
