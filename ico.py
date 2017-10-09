import csv
import json
from CoinmarketCap import CoinmarketCap


class ICO:
    def __init__(self, id, name, dataYesNo):
        self.id = id
        self.name = name
        self.data = []
        self.funds = dataYesNo

    def __str__(self):
        return str(self.funds)

    def hasData(self):
        return self.funds

ico_list = {}
coindesk_input = []
icobazaar_input = {}

baseAddress = 'Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\Listings'

# Source 1: Coindesk csv download
with open(baseAddress + '\CoinDesk+ICO+Database+-+Blockchain+ICOs-2017-09-26.csv') as file:
    reader = csv.reader(file)
    coindesk_input = list(reader)

for ico in coindesk_input:
    if ico[0] == 'Name':
        continue
    ico_name = str(ico[0]).lower()
    if ico_name in ico_list:
        ico_list[ico_name].data.append(ico)
    else:
        ico_list[ico_name] = ICO(ico_name, ico, True)


# Source 2: Coinmarketcap.com
coin = CoinmarketCap()
for key in coin.getCurrencies():
    if key in ico_list:
        print("CoinMarketCap " + key + " Already there")
    else:
        ico_list[str(key).lower()] = ICO(str(key).lower(), str(key).lower(), False)

# Source 3: IcoBazaar.com
with open(baseAddress + "\icobazaar-2017-09-26-11-16uhr.csv") as file:
    reader = csv.reader(file, delimiter=";")
    icobazaar_input = list(reader)

for ico in icobazaar_input:
    ico_name = str(ico[0]).lower()
    print("ICO Bazaar " + ico_name)
    if ico_name == 'Name':
        continue
    if ico_name in ico_list:
        print("CoinBazar: " + ico_name + " Already there")
        ico_list[ico_name].data.append(ico)
    else:
        ico_list[ico_name] = ICO(ico_name, ico, True)


# Source 4: https://icotracker.net/past
with open(baseAddress + "\icoTrackerArray.json") as file:
    icotracker_input = json.loads(file.read(), encoding="UTF-8")

    for ico_name in icotracker_input:
        ico_name = str(ico_name).lower()
        if ico_name in ico_list:
            print("ICO Tracker: " + ico_name + " Already there")
            ico_list[ico_name].data.append(ico)
        else:
            ico_list[ico_name] = ICO(ico_name, ico, False)


# Source 5: https://www.coinschedule.com/icos.php
with open(baseAddress + "\coinschedule-icos-2016-09-26.csv") as file:
    reader = csv.reader(file, delimiter=";")
    coinschedule_input = list(reader)

for ico in coinschedule_input:
    ico_name = str(ico[0]).lower()
    print("ICO Coinschedule " + ico_name)
    if ico_name == 'Name':
        continue
    if ico_name in ico_list:
        print("Coinschedule: " + ico_name + " Already there")
        ico_list[ico_name].data.append(ico)
    else:
        ico_list[ico_name] = ICO(ico_name, ico, True)

# Log all ico data
count = 0
total = 0
for key in sorted(ico_list):
    total += 1
    if ico_list[key].hasData():
        count += 1
    print(key + " : " + str(ico_list[key]))

print(count)
print(total)
