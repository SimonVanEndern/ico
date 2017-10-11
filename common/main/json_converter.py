from json import JSONEncoder

from ico.initial_coin_offering import ICO


class JsonConverter(JSONEncoder):
    def default(self, o):
        if isinstance(o, ICO):
            return o.__dict__
