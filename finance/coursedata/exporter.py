import csv


class Exporter:
    market_cap_string = "market_cap_by_available_supply"
    price_usd_string = "price_usd"
    price_btc_string = "price_btc"
    volume_string = "volume_usd"

    def export(self, json_data, path):
        market_cap = json_data[self.market_cap_string]
        market_cap_time, market_cap_data = zip(*market_cap)

        price_usd = list(json_data[self.price_usd_string])
        price_usd_time, price_usd_data = zip(*price_usd)

        price_btc = list(json_data[self.price_btc_string])
        price_btc_time, price_btc_data = zip(*price_btc)

        volume_usd = list(json_data[self.volume_string])
        volume_usd_time, volume_usd_data = zip(*volume_usd)

        assert(market_cap_time == price_btc_time == price_usd_time == volume_usd_time)

        output = zip(market_cap_time, price_usd_data, price_btc_data, volume_usd_data, market_cap_data)

        with open(path, "w") as file:
            writer = csv.writer(file, delimiter=',', lineterminator='\n')
            writer.writerow(["Timestamp", "USD", "BTC", "Volume", "MarketCap"])
            for row in output:
                writer.writerow(row)

        print("Written: " + path)
