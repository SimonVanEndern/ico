from typing import Tuple

import pandas

from common.currency import Currency


class CurrencyStatisticalData:
    def __init__(self, currency: Currency):
        self.currency: Currency = currency

        self.total_volume: float
        self.average_volume: float
        self.volume_linear_regression: Tuple(float, float)

        self.average_market_capitalization: float
        self.market_capitalization_linear_regression: Tuple(float, float)

        self.average_price: float
        self.price_linear_regression: Tuple(float, float)

        self.highest_price_difference: float
        self.price_change_from_beginning: float

        self.volatility: pandas.DataFrame
        self.volatility_linear_regression: Tuple(float, float)

        self.google_trends_correlations: dict

        self.percentage_of_total_market_capitalization: pandas.DataFrame

        self.volume_return_correlations: dict
        self.price_market_capitalization_correlation: float
