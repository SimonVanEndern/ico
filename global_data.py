from datetime import datetime


class GlobalData:
    financial_data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ico_data_path = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ico_static_date = "02.10.2017"
    ico_use_static_date = True

    download_raw_data_path_external = "X:\\bachelor-thesis\data"
    aggregated_data_path_external = "X:\\bachelor-thesis\\aggregated"
    reduced_data_path_external = "X:\\bachelor-thesis\\reduced"
    save_path_additional_data = "X:\\bachelor-thesis\\additional"

    last_date_for_download = int(datetime.strptime("12.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)

    coin_market_cap_graph_api_url = "graphs.coinmarketcap.com"

