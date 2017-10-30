from typing import Tuple

import pandas
import scipy
from scipy import stats

from common.time_series import TimeSeries, get_timeseries_with_same_datapoints


def calculate_linear_regression(data: TimeSeries) -> Tuple[float, float, float, float, float]:
    return stats.linregress(data.timestamps, data.data)


def calculate_correlation_for_timeseries(data1: TimeSeries, data2: TimeSeries) -> Tuple[float, float]:
    time_series_1, time_series_2 = get_timeseries_with_same_datapoints(data1, data2)

    return scipy.stats.pearsonr(time_series_1, time_series_2)

# def calculate_relative_change_smoothed(data, smoothing=30):
#     last = [data[0]]
#     output = []
#     for index, course in enumerate(data):
#
#         if index < smoothing:
#             # Not yet reached enough data
#             last.append(course)
#             continue
#
#         if (last[len(last) - smoothing]) == 0:
#
#             # Start with 0
#             output.append(0)
#         else:
#             output.append((course / last[len(last) - smoothing] - 1) / smoothing)
#
#         last.append(course)
#
#     return output
