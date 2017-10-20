import numpy

from common.currency_handler import CurrencyHandler


class Aggregator:
    currency_handler = CurrencyHandler()

    # Do stuff only for currencies where it makes sense.

    def check_all_currencies(self):
        for currency in self.currency_handler.get_all_currency_names_where_data_is_available():
            self.currency_handler.get_currency(currency)

    def get_volume_price_correlation(self):
        currencies = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=10000)
        correlations = []
        for index, currency in enumerate(currencies):
            if index in range(100, 10000, 100):
                print("Aggregator at " + str(index))
            total_correlation = self.currency_handler.get_currency(currency).calculate_volume_return_correlation()
            since_2016_correlation = self.currency_handler.get_currency(currency,
                                                                        date_limit="01.01.2016").calculate_volume_return_correlation()
            since_2017_correlation = self.currency_handler.get_currency(currency,
                                                                        date_limit="01.01.2017").calculate_volume_return_correlation()
            since_second_half_2017_correlation = self.currency_handler.get_currency(currency,
                                                                                    "01.07.2017").calculate_volume_return_correlation()

            correlations.append(
                (total_correlation, since_2016_correlation, since_2017_correlation, since_second_half_2017_correlation))
            # print(correlations[len(correlations) - 1])

        correlations = map(lambda x: (x[0][0], x[1][0], x[2][0], x[3][0]), correlations)
        total, since_2016, since_2017, second_2017 = zip(*correlations)
        # total = map(lambda x: x[0], total)
        # since_2016 = map(lambda )
        # print(sum(total))
        # print(sum(since_2016))
        # print(sum(since_2017))
        # print(sum(second_2017))

        return {"total": sum(total) / len(total),
                "since_2016": sum(since_2016) / len(since_2016),
                "since_2017": sum(since_2017) / len(since_2017),
                "second_2017": sum(second_2017) / len(second_2017)}

    def get_volume_price_aggregation_2(self, size_limit=10):
        limits = [None, "01.01.2016", "01.01.2017", "01.07.2017"]
        smoothings = [1, 2, 3, 5, 10]

        currencies = self.currency_handler.get_all_currency_names_where_data_is_available(size_limit=size_limit)
        output = {}
        for limit in limits:
            output[str(limit)] = []
            for name in currencies:
                dataset = []
                for smoothing in smoothings:
                    currency = self.currency_handler.get_currency(name, date_limit=limit)
                    data = currency.calculate_volume_return_correlation(smoothing)[0]

                    dataset.append(data)

                output[str(limit)].append(tuple(dataset))

        summary = {}

        for key, value in output.items():
            sm1, sm2, sm3, sm5, sm10 = zip(*value)
            summary[key] = (numpy.mean(sm1), numpy.mean(sm2), numpy.mean(sm3), numpy.mean(sm5), numpy.mean(sm10))

        return summary

# run_script = Aggregator()
# run_script.check_all_currencies()
