import sys
sys.path.insert(1, '../')
from core.Network import *
from core.functions import *

net = Network("../resources_exam/full_network.json")            # FULL NODES
# net = Network("../resources_exam/not_full_network.json")      # NOT-FULL NODES
net.connect()
net.weighted_paths_dataframe()
net.route_space_dataframe()
net.draw()

# transceiver = "fixed_rate"      # CHANGE IN THE NETWORK !!!!!!!!!!!
# transceiver = "flex_rate"
# transceiver = "shannon"
M = 3

conn_list = []
n_nodes = len(net.nodes)
traffic_matrix = np.zeros((n_nodes, n_nodes))

while np.count_nonzero(traffic_matrix) == 0:
    traffic_matrix = np.ones((n_nodes, n_nodes)) * 100e9 * M
    np.fill_diagonal(traffic_matrix, 0)
    conn_list = net.request_traffic_matrix(traffic_matrix)
    # print(net.route_space)
    # print(net.weighted_path)
    # net.route_space.to_csv("../results/MC_method1/full_network/"+transceiver+"/single_MC_run/route_space_snr.csv")
    # net.weighted_path.to_csv("../results/MC_method1/full_network/"+transceiver+"/single_MC_run/weighted_path.csv")
    net.reset_network()
    M += 1

    # Increments M until it can propagate all connections. When it succeeds in instantiating them all,
    # it stops increasing, the matrix becomes null and exits the cycle.
    # FULL_NETWORK (same thing for NOT_FULL but change the TOTAL_CAPACITY)
    # FIXED_RATE -> M = 3
    # FLEX_RATE  -> M = 9
    # SHANNON    -> M = 38


print("Maximum M: " + str(M-1))
print("Maximum bit rate: " + str(get_max_bit_rate(conn_list) / 1e9) + " Gbps")
print("Minimum bit rate: " + str(get_min_bit_rate(conn_list) / 1e9) + " Gbps")
print("Average bit rate: " + str(get_average_bit_rate(conn_list) / 1e9) + " Gbps")
print("Total capacity: " + str(get_total_capacity(conn_list) / 1e9) + " Gbps")

# plot_distribution(conn_list, "bit_rate", "../results/MC_method1/full_network/"+transceiver+"/single_MC_run/bit_rate_distribution.png")
# plot_distribution(conn_list, "latency", "../results/MC_method1/full_network/"+transceiver+"/single_MC_run/latency_distribution.png")
