from datetime import datetime


class GlobalData:
    financial_data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ico_data_path = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ico_static_date = "05.11.2017"
    ico_use_static_date: bool = True

    EXTERNAL_PATH_RAW_DATA = "X:\\bachelor-thesis\\raw-data"
    EXTERNAL_PATH_COMPRESSED_DATA = "X:\\bachelor-thesis\\compressed-data"
    EXTERNAL_PATH_AGGREGATED_DATA = "X:\\bachelor-thesis\\final-aggregated-data"
    EXTERNAL_PATH_ADDITIONAL_DATA = "X:\\bachelor-thesis\\additional-data"

    FOLDER_COMPRESSED_DATA_ONLY_RAW_DATA = "only-with-raw-data"
    FOLDER_COMPRESSED_DATA_WITH_ADDITIONAL_DATA = "with-additional-data"

    EXTERNAL_PATH_GOOGLE_TRENDS_DATA = "X:\\bachelor-thesis\google-trends"
    FOLDER_GOOGLE_TRENDS_6MONTHLY = "6monthly"
    RELATIVE_GOOGLE_TRENDS_DATA_PATH = "X:\\bachelor-thesis\google-trends\\relative"

    CURRENCY_HANDLER_PATH = "X:\\bachelor-thesis\currency-handler"

    ICO_FUNDING_AND_START_DATA_PATH = "X:\\bachelor-thesis\ico-data"

    EXTERNAL_PATH_ANALYSIS_DATA = "X:\\bachelor-thesis\\analysis"
    EXTERNAL_PATH_ANALYSIS_DATA_TODAY = None

    last_date_for_download: int = int(datetime.strptime("01.11.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    last_date_for_download2: int = int(datetime.strptime("01.11.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    last_date_for_analysis: int = int(datetime.strptime("31.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    TEST_LAST_DATE_FOR_DOWNLOAD: int = int(datetime.strptime("19.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)

    coin_market_cap_graph_api_url = "graphs.coinmarketcap.com"





