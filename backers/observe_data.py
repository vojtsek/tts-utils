import pandas
import sys
import numpy


if __name__ == '__main__':
    all_data = numpy.zeros((0, 3))
    files = sys.argv[1:]
    for csvf in files:
        data = pandas.read_csv(csvf, header=None)
        fns = numpy.array([[csvf] for _ in range(data.shape[0])])
        data = numpy.concatenate((fns, data), axis=1)
        all_data = numpy.concatenate((all_data, data), axis=0)
        # available_counts = numpy.unique(data['count'].values)
    synthesizers = numpy.unique(all_data[:,0])
    distinct_files = numpy.unique(all_data[:,1])
    means = []
    stds = []
    for f in distinct_files:
       f_data = all_data[all_data[:, 1] == f]
       mean = numpy.mean(f_data[:, 2])
       std = numpy.std(f_data[:, 2])
       means.extend([mean for _ in range(f_data.shape[0])])
       stds.extend([std] * f_data.shape[0])
    all_data = numpy.concatenate((all_data, numpy.array([means]).T), axis=1)
    all_data = numpy.concatenate((all_data, numpy.array([stds]).T), axis=1)
    sort_perm_mean = numpy.argsort(all_data[:, 3], axis=0)
    sort_perm_std = numpy.argsort(all_data[:, 4], axis=0)
    print(all_data[sort_perm_mean, 1])
