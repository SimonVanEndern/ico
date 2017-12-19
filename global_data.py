from datetime import datetime


class GlobalData:
    FINANCIAL_DATA_PATH = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ICO_DATA_PATH = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ICO_STATIC_DATE = "05.11.2017"
    ICO_USE_STATIC_DATE: bool = True

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

    EXTERNAL_PATH_ANALYSIS_DATA = "X:\\bachelor-thesis\\analysis"
    EXTERNAL_PATH_ANALYSIS_DATA_TODAY = None

    LAST_DATA_FOR_DOWNLOAD: int = int(datetime.strptime("01.12.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    LAST_DATA_FOR_DOWNLOAD_2: int = int(datetime.strptime("01.11.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    LAST_DATE_FOR_ANALYSIS: int = int(datetime.strptime("31.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
    TEST_LAST_DATE_FOR_DOWNLOAD: int = int(datetime.strptime("19.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)

    COIN_MARKET_CAP_GRAPH_API_URL = "graphs.coinmarketcap.com"
