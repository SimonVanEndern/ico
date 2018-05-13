from common.coinmarketCapApi import CoinmarketCapApi


class CurrencyNameMatcher:

    def __init__(self):
        self.coinmarketcap_source = CoinmarketCapApi()
        self.currency_map = self.coinmarketcap_source.getIdToSymbolMapping()
        self.currency_map_reverse = self.coinmarketcap_source.getIdToSymbolMapping(reverse=True)

    def match(self, input_dict):
        output = {}
        for key, value in input_dict.items():
            if key.lower() in self.currency_map:
                output[self.currency_map[key.lower()]] = value
            else:
                if key.upper() in self.currency_map_reverse:
                    output[key.upper()] = value
                else:
                    output[key.lower()] = value

        return output

    def unmatch_symbol(self, input_dict):
        output = {}
        for key, value in input_dict.items():
            if key in self.currency_map_reverse:
                output[self.currency_map_reverse[key]] = value
            else:
                output[key] = value

        return output
