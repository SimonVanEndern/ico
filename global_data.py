from datetime import datetime


class GlobalData:
    financial_data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ico_data_path = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ico_static_date = "02.10.2017"
    ico_use_static_date = True

    EXTERNAL_PATH_RAW_DATA = "X:\\bachelor-thesis\data"
    EXTERNAL_PATH_REDUCED_DATA = "X:\\bachelor-thesis\\reduced"
    EXTERNAL_PATH_AGGREGATED_DATA = "X:\\bachelor-thesis\\aggregated"
    EXTERNAL_PATH_ADDITIONAL_DATA = "X:\\bachelor-thesis\\additional"

    EXTERNAL_PATH_GOOGLE_TRENDS_DATA = "X:\\bachelor-thesis\google-trends"

    last_date_for_download = int(datetime.strptime("12.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)

    coin_market_cap_graph_api_url = "graphs.coinmarketcap.com"

