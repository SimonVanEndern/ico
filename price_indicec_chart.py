import matplotlib.pyplot as plt
import numpy
import pandas


class PriceIndicesChart:
    def __init__(self):
        crix = pandas.read_csv("Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\top\crix.csv", index_col=0)
        indices = pandas.read_csv("Z:\Google Drive\\05 - Projekte\\bachelor-thesis\\final-indices-2017-12-03-30-day-weighting.csv",
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
        total: pandas.DataFrame = pandas.concat([crix, indices[list(numpy.array(indices.columns))]], axis=1)
        # total.index = total.index.as_type("datetime64[s]")

        total.index = pandas.to_datetime(total.index, unit="ms")
        # total.plot(ax=ax)
        fig.set_size_inches(7, 3)

        print(total.columns)
        total[numpy.array(total.columns)[:15]].plot(ax=ax)
        fig.subplots_adjust(bottom=0.3)
        plt.legend(prop={"size": 7})
        plt.show()


PriceIndicesChart()
