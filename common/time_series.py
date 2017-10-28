from typing import Tuple, List

from common.data_point import from_tuple, DataPoint


class TimeSeries:
    # Tested
    def __init__(self, data):
        self.time_series: List(DataPoint) = list()
        self.time_series_dict: dict = dict()
        self.timestamps: List(int) = list()
        self.data: List(int) = list()

        self.relative_change = list()
        self.relative_change_dict = dict()

        if data is not None:
            if data[0] == ("timestamp", "data"):
                self.init_from_raw(data, starting_point=1)
            else:
                self.init_from_raw(data)

            self.sort()

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return str(self)

    def __eq__(self, other: 'TimeSeries'):
        return self.__dict__ == other.__dict__

    def sort(self):
        self.timestamps.sort()
        self.data.sort()
        self.time_series.sort()

    # Tested
    def add_data_point(self, point: DataPoint) -> None:
        self.time_series.append(point)
        self.time_series_dict[point.timestamp] = point

        self.timestamps.append(point.timestamp)
        self.data.append(point.data)

        self.sort()

    def init_from_raw(self, data, starting_point=0):
        if len(data[starting_point]) != 2:
            raise Exception("Wrong format")

        if isinstance(data[starting_point][0], str):
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
            self.timestamps.append(point[0])
            self.data.append(point[1])
            data_point = from_tuple(point)
            self.time_series.append(data_point)
            self.time_series_dict[data_point.timestamp] = data_point

    # Tested
    def get_first_timestamp(self) -> int:
        return self.timestamps[0]

    # Tested
    def has_gaps(self, step=1000 * 3600 * 24) -> bool:
        for i in range(0, len(self.timestamps) - 1):
            span = self.timestamps[i + 1] - self.timestamps[i]
            if span > step:
                return True

        return False

    # Tested
    def number_of_gaps(self, step=1000 * 3600 * 24) -> int:
        number_gaps = 0
        for i in range(0, len(self.timestamps) - 1):
            span = self.timestamps[i + 1] - self.timestamps[i]
            if span > step:
                number_gaps += 1

        return number_gaps

    def calculate_relative_change(self):
        iterator = iter(self.time_series)
        previous: DataPoint = next(iterator)
        for point in iterator:
            relative_change = previous.get_relative_change(point)
            relative_change_datapoint = DataPoint(point.timestamp, relative_change)

            self.relative_change.append(relative_change_datapoint)
            self.relative_change_dict[point.timestamp] = relative_change_datapoint

            previous = point

        return self.relative_change

    def calculate_relative_change_smoothed(self, smoothing=30) -> 'TimeSeries':
        previous = self.time_series[0]
        output = TimeSeries(None)
        for index, data_point in enumerate(self.time_series):

            if index < smoothing:
                # Not yet reached enough data
                continue

            if index == smoothing:

                # Start with 0
                output.add_data_point(DataPoint(data_point.timestamp, 0))
            else:

                output.add_data_point(DataPoint(data_point.timestamp, data_point.get_relative_change(previous)))
                previous = self.time_series[index - smoothing]

        return output


def get_timeseries_with_same_datapoints(first: TimeSeries, second: TimeSeries) -> Tuple[TimeSeries, TimeSeries]:
    all_timestamps = first.timestamps + second.timestamps

    new_first = TimeSeries(None)
    new_second = TimeSeries(None)

    for timestamp in all_timestamps:

        if timestamp in first.timestamps and timestamp in second.timestamps:
            new_first.add_data_point(first.time_series_dict[timestamp])
            new_second.add_data_point(second.time_series_dict[timestamp])

    return new_first, new_second
