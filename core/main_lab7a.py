from Network import *
from Connection import *
import matplotlib.pyplot as plt
import random  # useful to generate random combination of nodes

Net4 = Network("../resources/nodes_full.json")  # first read the matrix FULL
Net4.connect()  # recall connect to create the Network
# Net4.draw()     # draw the Network
Net4.weighted_paths_dataframe()  # recall weighted_paths to calculate the latency and snr of paths
Net4.route_space_dataframe()

node_list = list(Net4.nodes.keys())  # the elements of dictionary "nodes" are taken and insert in a list "node_list"
connection_obj_list = []  # list of instances of class connection
given_data = {}  # data given to the class connection -> dictionary
signal_power = 1  # signal_power equal to 1mW


# Now I have to create 100 connections, and then I can use the method "stream" to find latency and snr------------------
for i in range(100):
    io_nodes = random.sample(node_list, 2)  # It means -> from node_list rake two random values
    given_data["input"] = io_nodes[0]  # define the attributes of connection object...
    given_data["output"] = io_nodes[1]
    given_data["signal_power"] = signal_power

    objConnection = Connection(given_data)  # ...and now create the object with that attributes
    connection_obj_list.append(objConnection)  # Now the list of instances for 100 connection is created!

# Now I use the "stream" method to calculate the best latency and snr for all the 100 ----------------------------------
Net4.stream(connection_obj_list, signal_power, key="latency")
'''
latency_list = []
for conn in connection_obj_list:
    latency_list.append(conn.latency)
'''
# I recall the method stream now for the SNR (100 instances)------------------------------------------------------------
Net4.stream(connection_obj_list, signal_power, key="snr")
snr_list = []
for conn in connection_obj_list:
    if conn.snr != 0:
        snr_list.append(conn.snr)

# Draw the histograms---------------------------------------------------------------------------------------------------

# How many paths are deployed and with what latency
'''
plt.figure()
plt.hist(latency_list, color='b')
plt.xlabel("Latency [s]")
plt.ylabel("Number of times")
plt.title("Distribution of the latency")
'''
# How many paths are deployed and with what SNR
plt.figure()
plt.hist(snr_list, color='r')
plt.xlabel("snr [dB]")
plt.ylabel("Number of times")
plt.title("Distribution of the Signal_to_Noise Ratio (SNR)")
plt.savefig('../results/Nodes_full_json_SNR_distribution_')

plt.show()
