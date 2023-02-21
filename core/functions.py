import matplotlib.pyplot as plt
import sys


def get_max_bit_rate(connections):
    max_br = 0
    for conn in connections:
        if conn.bit_rate > max_br:
            max_br = conn.bit_rate
    return max_br


def get_min_bit_rate(connections):
    min_br = sys.maxsize        # report the max size of the variable
    for conn in connections:
        if conn.bit_rate < min_br and conn.bit_rate != 0:
            min_br = conn.bit_rate
    return min_br


def get_average_bit_rate(connections):
    sum_br = 0
    br_none = 0
    for conn in connections:
        if conn.bit_rate != 0:
            sum_br += conn.bit_rate
        else:
            br_none += 1
    return sum_br / (len(connections) - br_none)


def get_total_capacity(connections):
    sum_br = 0
    for conn in connections:
        sum_br += conn.bit_rate
    return sum_br


def get_snr_conn(connections):
    snr_conn = []
    for conn in connections:
        if conn.snr is not None:
            snr_conn.append(conn.snr)
    return snr_conn


def get_conn_rejected(connections):
    conn_rejected = 0
    for conn in connections:
        if conn.snr is None:
            conn_rejected += 1
    return conn_rejected


def plot_distribution(connections, parameter, filename):
    values = []
    for conn in connections:
        values.append(getattr(conn, parameter))

    plt.figure()
    plt.hist(values)
    plt.xlabel(parameter)
    plt.ylabel("Occurrences")
    plt.title("Distribution of " + parameter)
    plt.savefig(filename)


def plot_distribution_values(values, parameter, title, filename):

    plt.figure()
    plt.hist(values)
    plt.xlabel(parameter)
    plt.ylabel("Occurrences")
    plt.title(title)
    plt.savefig(filename)
    plt.show()


def plot_snr(values, parameter, title, filename):

    plt.figure()
    plt.hist(values, bins=20)
    plt.xlabel(parameter)
    plt.ylabel("Occurrences")
    plt.title(title)
    plt.savefig(filename)
    plt.show()
