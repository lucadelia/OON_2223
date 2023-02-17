import sys
sys.path.insert(1, '../')
from core.Network import *
from core.functions import *

for i in range(3):
    if i == 0:
        transceiver = "fixed_rate"
        M = 5
    elif i == 1:
        transceiver = "flex_rate"
        M = 17
    else:
        transceiver = "shannon"
        M = 76

    net = Network("../resources/nodes_full_"+transceiver+".json")
    net.connect()
    net.weighted_paths_dataframe()
    net.route_space_dataframe()
    # M = 1

    conn_list = []
    n_nodes = len(net.nodes)
    traffic_matrix = np.zeros((n_nodes, n_nodes))

    while np.count_nonzero(traffic_matrix) == 0:
        traffic_matrix = np.ones((n_nodes, n_nodes)) * 100e9 * M
        np.fill_diagonal(traffic_matrix, 0)
        conn_list = net.request_traffic_matrix(traffic_matrix)
        # print(net.route_space)
        # print(net.weighted_path)
        net.reset_network()
        M += 1

        # Increments M until it can propagate all connections. When it succeeds in instantiating them all,
        # it stops increasing, the matrix becomes null and exits the cycle.
        # To avoid performing the increment cycle, I have displayed the required M at the top -> 5, 17, 76.

        # CHANGE WITH THE NEW NETWORK PROVIDED BY THE PROFESSOR !!!!!!!!!!!!!!

    print("Maximum M: " + str(M-1))
    print("Maximum bit rate: " + str(get_average_bit_rate(conn_list) / 1e9) + " Gbps")
    print("Total capacity: " + str(get_total_capacity(conn_list) / 1e9) + " Gbps")
    plot_distribution(conn_list, "bit_rate", "../old_results/Lab9/"+transceiver+"/bit_rate_distribution.png")
    plot_distribution(conn_list, "latency", "../old_results/Lab9/"+transceiver+"/latency_distribution.png")
