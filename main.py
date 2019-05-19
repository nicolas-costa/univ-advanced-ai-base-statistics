import matplotlib.pyplot as plt
import numpy as np
import csv
import os

data = []
attributes = {'Class': 0, 'Alcohol':1, 'Malic acid': 2, 'Ash':3, 'Alcalinity of Ash':4,
              'Magnesium': 5, 'Total phenols': 6, 'Flavanoids': 7, 'Nonflavanoids phenols': 8,
              'Proanthocyanins': 9,'Color intensity': 10, 'Hue': 11, 'OD280-OD315': 12, 'Proline': 13}
median = []
standard_deviation = []
classes = [
    [],
    [],
    []
]

colors = ['red', 'green', 'blue']

def load_data():
    global data

    with open((os.path.dirname(os.path.realpath(__file__)) + '/data/wine.data')) as datafile:
        data_reader = csv.reader(datafile, delimiter=',')

        for line in data_reader:
            data.append([float(i) for i in line])

    data = np.array(data)

def compute_data():
    global median, standard_deviation, totals

    median = np.median(data, axis=0).astype(dtype=np.float32)

    standard_deviation = np.std(data, axis=0, dtype=np.float32)

    for cls in data:

        if cls[0] == 1:
            classes[0].append(list(cls))
        elif cls[0] == 2:
            classes[1].append(list(cls))
        elif cls[0] == 3:
            classes[2].append(list(cls))

    classes[0] = np.array(classes[0])
    classes[1] = np.array(classes[1])
    classes[2] = np.array(classes[2])

def generate_data():
    global removed_noise, median, standard_deviation

    for label, idx in attributes.items():

        if label == 'Class':
            continue

        else:

            print(label + ' - ' + 'Median: ' + str(median[idx]) + ' | ' + 'Standard deviation: ' + str(standard_deviation[idx]))

            generate_data_images(label, idx)

    export_processed_data()

def generate_data_images(label, idx):
    global removed_noise, classes, colors

    plt.subplot(2, 1, 1)

    plt.title('Histogram of ' + label)

    plt.xlabel('Distribution')

    plt.ylabel('Frequency')

    plt.hist([classes[0][:, idx], classes[1][:, idx], classes[2][:, idx]],
             color=colors, stacked=True, alpha=0.5,
             range=(np.array(data[:, idx]).min(), np.array(data[:, idx]).max()),
             label=['Class 1', 'Class 2', 'Class 3'])

    plt.legend()

    plt.subplot(2, 1, 2)

    plt.title('Boxplot of ' + label)

    plt.xlabel('Distribution')

    plt.ylabel('Values')

    fliers = plt.boxplot([classes[0][:, idx], classes[1][:, idx], classes[2][:, idx]],
                labels=['Class 1', 'Class 2', 'Class 3'])['fliers']

    remove_noise((fliers[0].get_data(), fliers[1].get_data(), fliers[2].get_data()), idx)

    plt.tight_layout()

    plt.savefig(os.path.join('figs', label))

    plt.close()

def remove_noise(fliers:tuple, idx):
    global removed_noise, classes

    for cls in fliers:

        if len(cls[0]) > 0:

            normalized_index = (cls[0][0].astype(np.int) - 1)
            normalized_arr = classes[normalized_index][:, idx]

            n = np.nonzero(np.isin(normalized_arr, (cls[1][:])))

            classes[normalized_index] = np.delete(classes[normalized_index], n[0], axis=0)

def export_processed_data():
    global classes

    print('exporting processed base...')

    with open((os.path.dirname(os.path.realpath(__file__)) + '/data/processed_wine.data'), mode='w', newline='') as wine_data:
        csv_writer = csv.writer(wine_data, delimiter=',')

        for list in classes:
            for line in list:
                csv_writer.writerow(line)


def start():

    load_data()

    compute_data()

    generate_data()

if __name__ == '__main__':

    # do shit
    start()