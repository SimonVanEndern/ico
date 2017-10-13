import csv
from datetime import datetime

# with open("X:\\bachelor-thesis\\aggregated\\bitcoin.csv") as file:
#     reader = csv.reader(file)
#     data = list(reader)
#     for row in data:
#         if row[0] == "Timestamp":
#             continue
#         print(datetime.fromtimestamp(int(row[0]) / 1e3))

def get_data(i):
    return {"hey": i * 2}

def example():
    output = []
    for i in range(10):
        test = get_data(i)
        output.append(test)

    print(output)


example()
