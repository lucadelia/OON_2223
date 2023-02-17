import numpy as np

from Network import *
from Connection import *
import matplotlib.pyplot as plt
import random  # useful to generate random combination of nodes

# Net5 = Network("../resources/nodes_full_fixed_rate.json")
# Net5 = Network("../resources/nodes_full_flex_rate.json")
Net5 = Network("../resources/nodes_full_shannon.json")
Net5.connect()  # recall connect to create the Network
# Net4.draw()     # draw the Network
Net5.weighted_paths_dataframe()  # recall weighted_paths to calculate the latency and snr of paths
Net5.route_space_dataframe()

node_list = list(Net5.nodes.keys())  # the elements of dictionary "nodes" are taken and insert in a list "node_list"
connection_obj_list = []  # list of instances of class connection
given_data = {}  # data given to the class connection -> dictionary
signal_power = 1  # signal_power equal to 1mW


# Now I have to create 100 connections, and then I can use the method "stream" to find latency and snr------------------
for i in range(100):
    io_nodes = random.sample(node_list, 2)  # It means -> from node_list rake two random values
    given_data["input"] = io_nodes[0]       # define the attributes of connection object...
    given_data["output"] = io_nodes[1]
    given_data["signal_power"] = signal_power

    objConnection = Connection(given_data)      # ...and now create the object with that attributes
    connection_obj_list.append(objConnection)   # Now the list of instances for 100 connection is created!
'''
# Now I use the "stream" method to calculate the best latency and snr for all the 100 ----------------------------------
Net5.stream(connection_obj_list, signal_power, key="latency")
latency_list = []
for conn in connection_obj_list:
    latency_list.append(conn.latency)
'''
# I recall the method stream now for the SNR (100 instances)------------------------------------------------------------
Net5.stream(connection_obj_list, signal_power, key="snr")

bit_rate_values = []
rejected = []

for conn in connection_obj_list:
    if conn.snr is not None:
        bit_rate_values.append(conn.bit_rate)
    else:
        rejected += 1

print(bit_rate_values)

# Draw the histograms---------------------------------------------------------------------------------------------------

'''
# How many paths are deployed and with what latency
plt.figure()
plt.hist(latency_list, color='b')
plt.xlabel("Latency [s]")
plt.ylabel("Number of times")
plt.title("Distribution of the latency")
'''

# How many paths are deployed and with what SNR
plt.figure()
plt.hist(bit_rate_values, color='r')
plt.xlabel("Bit-Rate [Gbps]")
plt.ylabel("Number of times")
plt.title("Distribution of Bit-Rate (Br)")

# plt.savefig('../results/Distribution_Bit_Rate_FIXED_RATE')
# plt.savefig('../results/Distribution_Bit_Rate_FLEX_RATE')
plt.savefig('../results/Distribution_Bit_Rate_SHANNON')

# Calculate also the (1) average of the bit_rates and (2) the total capacity allocated in the network
bit_rate_average = np.mean(bit_rate_values)
tot_capacity = np.sum(bit_rate_values)
print('Rejected connections: ' + str(rejected) + ' Average Bit-Rate: ' + str(bit_rate_average) + ' Tot. capacity: ' + str(tot_capacity))

plt.show()
