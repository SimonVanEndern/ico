class DataPoint:
    def __init__(self, timestamp, data):
        self.timestamp = timestamp
        self.data = data

    def __lt__(self, other):
        if self.timestamp is None:
            return False
        else:
            if other.timestamp is None:
                return True
            else:
                return self.timestamp < other.timestamp

    def __str__(self):
        return str(self.__dict__)

    def __eq__(self, other: 'DataPoint'):
        return self.__dict__ == other.__dict__

    def __repr__(self):
        return str(self)

    def get_relative_change(self, second: 'DataPoint'):
        if self.data == 0:
            return 0
        else:
            return second.data / self.data - 1


def from_tuple(tuple_input) -> DataPoint:
    timestamp = int(tuple_input[0])

    if isinstance(tuple_input[1], str):
        try:
            data = int(tuple_input[1])
        except ValueError:
            data = float(tuple_input[1])
    else:
        data = tuple_input[1]

    return DataPoint(timestamp, data)
