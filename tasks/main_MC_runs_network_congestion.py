import sys
sys.path.insert(1, '../')
from statistics import mean
from core.Network import *
from core.functions import *

network_type = "full_network"
# network_type = "not_full_network"

net = Network("../resources_exam/"+network_type+".json")
net.connect()
net.weighted_paths_dataframe()
net.route_space_dataframe()
# net.draw()

transceiver = "fixed_rate"      # Remember to change in the network!
# transceiver = "flex_rate"
# transceiver = "shannon"

conn_list = []
n_nodes = len(net.nodes)
traffic_matrix = np.zeros((n_nodes, n_nodes))
list_conn_list8 = []
value_mean = []

MC = 0          # index
MC_runs = 3     # Number of Monte Carlo runs

M = 1
M_cycle = 10

# M = 3     # FIXED_RATE
# M = 9     # FLEX_RATE
# M = 38    # SHANNON

for M in range(M_cycle):
    list_rejected_MC = []
    for MC in range(MC_runs):
        print("Monte-Carlo run number: " + str(MC_runs-MC))
        # while np.count_nonzero(traffic_matrix) == 0:
        traffic_matrix = np.ones((n_nodes, n_nodes)) * 100e9 * M
        np.fill_diagonal(traffic_matrix, 0)
        conn_list = net.request_traffic_matrix(traffic_matrix)
        list_conn_list8.append(get_conn_rejected(conn_list))  # num of rejected
        net.reset_network()
    j = 0
    for j in list_conn_list8:
        list_rejected_MC.extend(j)
    value_mean.append(mean(list_rejected_MC))

# plot_graph(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]), value_mean, "Average rejected connection by increasing M value", "../results/MC_method2/" + network_type + "/" + transceiver + "/rejected_conn_MC_NOTFULL.png")
plot_graph(np.array([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]), value_mean, "Average rejected connection by increasing M value", "../results/MC_method2/" + network_type + "/" + transceiver + "/rejected_conn_MC_NOTFULL.png")
traffic_matrix = np.zeros((n_nodes, n_nodes))
