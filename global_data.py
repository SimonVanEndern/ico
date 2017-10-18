from datetime import datetime


class GlobalData:
    financial_data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ico_data_path = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ico_static_date = "02.10.2017"
    ico_use_static_date = True

    EXTERNAL_PATH_RAW_DATA = "X:\\bachelor-thesis\\raw-data"
    EXTERNAL_PATH_COMPRESSED_DATA = "X:\\bachelor-thesis\\compressed-data"
    EXTERNAL_PATH_AGGREGATED_DATA = "X:\\bachelor-thesis\\final-aggregated-data"
    EXTERNAL_PATH_ADDITIONAL_DATA = "X:\\bachelor-thesis\\additional-data"

    FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA = "only-with-raw-data"
    FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA = "with-additional-data"

    EXTERNAL_PATH_GOOGLE_TRENDS_DATA = "X:\\bachelor-thesis\google-trends"
    FOLDER_GOOGLE_TRENDS_6MONTHLY = "6monthly"

    CURRENCY_HANDLER_PATH = "X:\\bachelor-thesis\currency-handler"

    ICO_FUNDING_AND_START_DATA_PATH = "X:\\bachelor-thesis\ico-data"

    last_date_for_download = int(datetime.strptime("12.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)

    coin_market_cap_graph_api_url = "graphs.coinmarketcap.com"

