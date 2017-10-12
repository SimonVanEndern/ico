from datetime import datetime


class GlobalData:
    financial_data_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-10-08\\"
    ico_data_path = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

    ico_static_date = "02.10.2017"
    ico_use_static_date = True

    download_data_path_external = "X:\\bachelor-thesis\data"
    last_date_for_download = int(datetime.strptime("12.10.2017 10:00", "%d.%m.%Y %H:%M").timestamp() * 1e3)
