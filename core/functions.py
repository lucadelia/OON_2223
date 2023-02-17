import matplotlib.pyplot as plt


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


def plot_distribution(connections, parameter, filename):
    values = []
    for conn in connections:
        values.append(getattr(conn, parameter))

    plt.figure()
    plt.hist(values)
    plt.xlabel(parameter)
    plt.ylabel("Number of times")
    plt.title("Distribution of " + parameter)
    plt.savefig(filename)
