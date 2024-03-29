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

transceiver = "fixed_rate"      # Remember to change in the "Network"
# transceiver = "flex_rate"
# transceiver = "shannon"

M = 3       # FIXED_RATE
# M = 9     # FLEX_RATE
# M = 38    # SHANNON

MC = 0          # index
MC_runs = 30    # Number of Monte Carlo runs
conn_list = []
n_nodes = len(net.nodes)
traffic_matrix = np.zeros((n_nodes, n_nodes))
list_conn_list1 = []
list_conn_list2 = []
list_conn_list3 = []
list_conn_list4 = []
list_conn_list5 = []
list_conn_list6 = []
list_conn_list7 = []
list_conn_list8 = []

for MC in range(MC_runs):
    print("Monte-Carlo run number: " + str(MC_runs-MC))
    while np.count_nonzero(traffic_matrix) == 0:
        traffic_matrix = np.ones((n_nodes, n_nodes)) * 100e9 * M
        np.fill_diagonal(traffic_matrix, 0)
        conn_list = net.request_traffic_matrix(traffic_matrix)

        list_conn_list1.append(get_average_bit_rate(conn_list) / 1e9)   # [Gbps] This explains the "1e9"
        list_conn_list2.append(get_total_capacity(conn_list) / 1e9)     # [Gbps]
        list_conn_list3.append(get_max_bit_rate(conn_list) / 1e9)       # [Gbps]
        list_conn_list4.append(get_min_bit_rate(conn_list) / 1e9)       # [Gbps]
        list_conn_list5.append(get_snr_conn(conn_list))                 # [dB]
        list_conn_list6.append(get_max_lat(conn_list))                  # [s]
        # list_conn_list7.append(get_min_lat(conn_list))                # [s]
        list_conn_list8.append(get_conn_rejected(conn_list))            # num of rejected
        net.reset_network()
    traffic_matrix = np.zeros((n_nodes, n_nodes))

        # Increments M until it can propagate all connections. When it succeeds in instantiating them all,
        # it stops increasing, the matrix becomes null and exits the cycle.
        # FULL_NETWORK (same thing for NOT_FULL but change the TOTAL_CAPACITY)

# net.route_space.to_csv("../results/MC_method1/"+network_type+"/"+transceiver+"/route_space_snr.csv")
# net.weighted_path.to_csv("../results/MC_method1/"+network_type+"/"+transceiver+"/weighted_path.csv")

plot_distribution_values(list_conn_list1, "Average bit_rate [Gbps]", "Bit_rate distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/average_bit_rate_MC.png")
print("Average bit-rate for all the MC simulation: " + str(mean(list_conn_list1)))
plot_distribution_values(list_conn_list2, "Total capacity requested", "Capacity distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/capacity_distribution_MC.png")
print("Average total capacitance necessary for all the connections: " + str(mean(list_conn_list2)))
plot_distribution_values(list_conn_list3, "Average MAXIMUM bit_rate [Gbps]", "MAXIMUM Bit_rate distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/average_MAX_bit_rate_MC.png")
print("Average MAXIMUM bit-rate for all the MC simulation: " + str(mean(list_conn_list3)))
plot_distribution_values(list_conn_list4, "Average MINIMUM bit_rate [Gbps]", "MINIMUM Bit_rate distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/average_MIN_bit_rate_MC.png")
print("Average MINIMUM bit-rate for all the MC simulation: " + str(mean(list_conn_list4)))
plot_distribution_values(list_conn_list6, "Average MAXIMUM latency [s]", "MAXIMUM Latency distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/average_MAX_latency_MC.png")
print("Average MAXIMUM latency for all the MC simulation: " + str(mean(list_conn_list6)))
# plot_distribution_values(list_conn_list7, "Average MINIMUM latency [s]", "MINIMUM Latency distribution", "../results/MC_method1/"+network_type+"/"+transceiver+"/average_MIN_latency_MC.png")
# print("Average MINIMUM latency for all the MC simulation: " + str(mean(list_conn_list7)))

list_nsr_MC = []
i = 0
for i in list_conn_list5:
    list_nsr_MC.extend(i)
# print(list_nsr_MC)
plot_snr(list_nsr_MC, "SNR [dB]", "SNR Monte Carlo simulation", "../results/MC_method1/"+network_type+"/"+transceiver+"/SNR_MC.png")
print("Average SNR Monte Carlo: " + str(mean(list_nsr_MC)))

list_rejected_MC = []
j = 0
for j in list_conn_list8:
    list_rejected_MC.extend(j)
# print(list_rejected_MC)
plot_rejected(list_rejected_MC, "Number of rejected connections", "Rejected connection for MC runs", "../results/MC_method1/"+network_type+"/"+transceiver+"/rejected_conn_MC.png")
print("Average number of rejected connections: " + str(mean(list_rejected_MC)))

