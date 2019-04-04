import matplotlib.pyplot as plt
import numpy as np
import csv
import os

data = []
attributes = {'Class': 0, 'Alcohol':1, 'Malic acid': 2, 'Ash':3, 'Alcalinity of Ash':4,
              'Magnesium': 5, 'Total phenoids': 6, 'Flavanoids': 7, 'Nonflavanoids phenols': 8,
              'Color intensity': 9, 'Hue': 10, 'OD280/OD315': 11, 'Proline': 12}
median = []
standard_deviation = []
totals = []

def load_data():

    with open((os.path.dirname(os.path.realpath(__file__)) + '/data/wine.data')) as datafile:
        data_reader = csv.reader(datafile, delimiter=',')

        for line in data_reader:
            data.append([float(i) for i in line])

def compute_data():

    global median
    global standard_deviation
    global totals



    median = np.median(data, axis=0).astype(dtype=np.float32)

    standard_deviation = np.std(data, axis=0, dtype=np.float32)

    totals = np.sum(data, axis=0)


def show_data():

    skip = 0
    global median
    global standard_deviation

    for label, idx in attributes.items():

        if skip == 0:
            skip = skip + 1

            continue

        else:
            print(label + ' - ' + 'Median: ' + str(median[idx]) + ' | ' + 'Standard deviation: ' + str(standard_deviation[idx]))

    plt.subplot(2, 1, 1)

    plt.hist(totals[1:])

    plt.subplot(2, 1, 2)

    plt.boxplot(totals[1:])

    plt.show(block=True)

def start():

    load_data()

    compute_data()

    show_data()



if __name__ == '__main__':

    # do shit
    start()