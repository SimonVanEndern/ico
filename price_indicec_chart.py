import matplotlib.pyplot as plt
import numpy
import pandas


class PriceIndicesChart:
    def __init__(self):
        crix = pandas.read_csv("Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\top\crix.csv", index_col=0)
        indices = pandas.read_csv("Z:\Google Drive\\05 - Projekte\\bachelor-thesis\indices_first_try_4.csv",
                                  index_col=0)

        for index in crix.index:
            if index not in indices.index:
                crix = crix.drop(index)

        # Crix based on 1000 index points
        crix = crix / 10
        crix.columns = ["CRIX index"]

        first_crix_date = crix.index[0]

        for column in indices.columns:
            value_at_crix_first_date = indices[column][first_crix_date]

            indices[column] = indices[column] / value_at_crix_first_date * 100

        fig, ax = plt.subplots()
        ax.set_yscale("log")
        ax.set(xlabel="Time", ylabel="Index (logarithmic scaling)")
        # indices.plot(ax=ax)
        total: pandas.DataFrame = pandas.concat([crix, indices[list(numpy.array(indices.columns)[:7])]], axis=1)
        # total.index = total.index.as_type("datetime64[s]")

        total.index = pandas.to_datetime(total.index, unit="ms")
        # total.plot(ax=ax)
        plt.legend(prop={"size": 8})
        fig.set_size_inches(7, 3.5)

        total[numpy.array(total.columns)[:8]].plot(ax=ax)
        plt.show()


PriceIndicesChart()
