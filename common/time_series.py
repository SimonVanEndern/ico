from typing import Tuple, List

import pandas

from common.data_point import from_tuple, DataPoint


class TimeSeries:
    # Tested
    def __init__(self, data, step=1000 * 3600 * 24):
        self.step = step
        self.time_series: List(DataPoint) = list()
        self.time_series_dict: dict = dict()
        self.timestamps: List(int) = list()
        self.data: List(int) = list()

        self.relative_change_dict = dict()

        if data is not None:
            if data[0] == ("timestamp", "data"):
                self.init_from_raw(data, starting_point=1)
            else:
                self.init_from_raw(data)

        self.refresh()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'TimeSeries'):
        return self.time_series == other.time_series and self.time_series_dict == other.time_series_dict \
               and self.timestamps == other.timestamps and self.data == other.data

    def refresh(self):
        self.time_series.sort()
        self.timestamps = list(map(lambda x: x.timestamp, self.time_series))
        self.data = list(map(lambda x: x.data, self.time_series))

        self.pandas_datapoints = list()
        self.pandas_timestamps = list()
        if len(self.time_series) > 0:
            for i in (
                    range(self.time_series[0].timestamp,
                          self.time_series[len(self.time_series) - 1].timestamp + self.step,
                          self.step)):
                self.pandas_timestamps.append(i)
                if i in self.time_series_dict:
                    self.pandas_datapoints.append(self.time_series_dict[i].data)
                else:
                    self.pandas_datapoints.append(None)

            self.df: pandas.DataFrame = pandas.DataFrame(self.pandas_datapoints, index=self.pandas_timestamps)
        else:
            self.df = None

        self.relative_change = self.calculate_relative_change()

    # Tested
    def add_data_point(self, point: DataPoint) -> None:
        self.time_series.append(point)
        self.time_series_dict[point.timestamp] = point
        self.time_series_dict = dict(sorted(self.time_series_dict.items()))

        self.refresh()

    def init_from_raw(self, data, starting_point=0):
        if len(data[starting_point]) != 2:
            raise Exception("Wrong format")

        if isinstance(data[starting_point][0], str) or isinstance(data[starting_point][1], str):
            self.init_from_string_representation(data)

        elif isinstance(data[starting_point][0], int) or isinstance(data[starting_point][0], float):
            self.init_from_number_representation(data, starting_point=starting_point)

    def init_from_string_representation(self, data):
        try:
            number_data = list(map(lambda x: (int(x[0]), int(x[1])), data))
        except ValueError:
            number_data = list(map(lambda x: (int(x[0]), float(x[1])), data))

        self.init_from_number_representation(number_data)

    def init_from_number_representation(self, data, starting_point=0):
        for index, point in enumerate(data):
            if index < starting_point:
                continue
            data_point = from_tuple(point)
            self.time_series.append(data_point)
            self.time_series_dict[data_point.timestamp] = data_point

    # Tested
    def get_first_timestamp(self) -> int:
        return self.timestamps[0]

    # Tested
    def has_gaps(self) -> bool:
        return self.df.isnull().values.any()

    # Tested
    def number_of_gaps(self) -> int:
        return self.df.isnull().values.sum()

    def calculate_relative_change(self) -> pandas.DataFrame:
        if self.df is not None:
            return self.df.interpolate(limit=1).pct_change()

    def calculate_relative_change_smoothed(self, smoothing=30) -> pandas.DataFrame:
        return self.df.interpolate(limit=1).pct_change(periods=smoothing) / smoothing


def get_timeseries_with_same_datapoints(first: TimeSeries, second: TimeSeries) -> Tuple[TimeSeries, TimeSeries]:
    all_timestamps = first.timestamps + second.timestamps

    new_first = TimeSeries(None)
    new_second = TimeSeries(None)

    for timestamp in all_timestamps:

        if timestamp in first.timestamps and timestamp in second.timestamps:
            new_first.add_data_point(first.time_series_dict[timestamp])
            new_second.add_data_point(second.time_series_dict[timestamp])

    return new_first, new_second
