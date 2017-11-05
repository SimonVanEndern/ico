import logging


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
        self.logger = logging.getLogger(self.__class__.__name__)

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
        if self.__dict__ == other.__dict__:
            return True
        if self.compare_relaxed(other):
            self.logger.warning("Different double value")
            return True

    def __eq__(self, other):
        return self.__cmp__(other)

    def compare_relaxed(self, other: 'DatapointDTO'):
        for first, second in [(self.timestamp, other.timestamp),
                              (self.market_cap, other.market_cap),
                              (self.usd, other.usd),
                              (self.volume, other.volume),
                              (self.btc, other.btc)]:
            if first != second and first != 0 and second != 0:
                return False

        return True

    def add_volume(self, volume_tuple):
        if volume_tuple[0] == self.timestamp:
            if self.volume is not None:
                if self.volume != volume_tuple[1]:
                    raise Exception("Different USD values")
            self.volume = volume_tuple[1]
        else:
            return False

    def add_btc(self, btc_tuple):
        if btc_tuple[0] == self.timestamp:
            if self.btc is not None:
                if self.btc != btc_tuple[1]:
                    raise Exception("Different USD values")
            self.btc = btc_tuple[1]
        else:
            return False

    def add_usd(self, usd_tuple):
        if usd_tuple[0] == self.timestamp:
            if self.usd is not None:
                if self.usd != usd_tuple[1]:
                    raise Exception("Different USD values")
            self.usd = usd_tuple[1]
        else:
            return False
