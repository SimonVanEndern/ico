import sqlite3

conn = sqlite3.connect("ico.db")

print("Opened database successfully")

conn.execute('''Create TABLE BitcoinPrices
            (ID INT PRIMARY KEY NOT NULL,
            PRICE INT NOT NULL,
            MARKETCAP INT NOT NULL)''')

conn.execute("INSERT INTO BitcoinPrices (ID, PRICE, MARKETCAP) \
              VALUES (1111, 1, 1)")

conn.close()