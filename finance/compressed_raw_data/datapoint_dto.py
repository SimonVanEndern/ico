def from_market_cap(market_cap_tuple):
    return DatapointDTO(market_cap_tuple[0], market_cap_tuple[1], None, None, None)


def from_usd(price_tuple):
    return DatapointDTO(price_tuple[0], None, price_tuple[1], None, None)


def from_btc(price_tuple):
    return DatapointDTO(price_tuple[0], None, None, price_tuple[1], None)


def from_volume(volume_tuple):
    return DatapointDTO(volume_tuple[0], None, None, None, volume_tuple[1])


class DatapointDTO:
    def __init__(self, timestamp, market_cap, usd, btc, volume):
        self.timestamp = timestamp
        self.market_cap = market_cap
        self.usd = usd
        self.volume = volume
        self.btc = btc

    def __repr__(self):
        return str(self)

    def __str__(self):
        return str([self.timestamp, self.market_cap, self.usd, self.btc, self.volume])

    def __cmp__(self, other):
        return self.__dict__ == other.__dict__

    def __eq__(self, other):
        return self.__cmp__(other)

    def add_volume(self, volume_tuple):
        if volume_tuple[0] == self.timestamp:
            self.volume = volume_tuple[1]
        else:
            return False

    def add_btc(self, btc_tuple):
        if btc_tuple[0] == self.timestamp:
            self.btc = btc_tuple[1]
        else:
            return False

    def add_usd(self, usd_tuple):
        if usd_tuple[0] == self.timestamp:
            self.usd = usd_tuple[1]
        else:
            return False
