import re


def parse_px_data(filepath, prefix, column, time_column=1):
    times = []
    data = []

    file = open(filepath)

    for line in file.readlines():
        if re.match(r'%s,.+' % prefix, line):
            split = line.strip().split(",")
            times.append(int(split[time_column]) / 1e6)
            data.append(float(split[time_column + 1 + column]))

    file.close()
    return times, data


def parse_ard_data(filepath, column):
    times = []
    data = []

    file = open(filepath)
    for line in file.readlines():
        split = line.strip().split(",")
        times.append(int(split[0]) / 1e3)
        data.append(float(split[1 + column]))

    file.close()
    return times, data
