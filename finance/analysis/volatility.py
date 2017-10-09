import pandas
import numpy
import os.path
import matplotlib.pyplot as plt
import os


class Volatility:

    example_path = "Z:\Google Drive\\01 - Studium\Bachelorarbeit\data\coinmarketcap-2017-09-28"
    example_currency = "bitcoin"

    def __init__(self):
        data_frame = pandas.read_csv(os.path.join(self.example_path, self.example_currency + ".csv"))
        df = data_frame
        print(df.columns)
        # rolling_30 = pandas.DataFrame.rolling(df["USD"], window=30, min_periods=30)
        # rolling_60 = pandas.DataFrame.rolling(df["USD"], window=60, min_periods=60)
        # rolling_mean_30 = rolling_30.mean()
        # rolling_mean_60 = rolling_60.mean()
        # rolling_mean_30.plot()
        # rolling_mean_60.plot()
        # rolling_30.std().plot()
        # plt.show()
        return

    def multiple_data(self):
        print("Hello")
        for idx, filename in enumerate(os.listdir(self.example_path)):
            print(filename)
            if idx == 20:
                break

            df = pandas.read_csv(os.path.join(self.example_path, filename))
            rolling_30_mean = pandas.DataFrame.rolling(df["Volume"], window=30, min_periods=30).mean()
            rolling_30_mean.plot().set_ylim(0, 50000000)

        plt.show()


vol = Volatility()
vol.multiple_data()
