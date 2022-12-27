# main Lab2 -> main that construct the network and run "stream" method over 100 connection with signal_power = 1mW
# Input/Output randomly chosen. Plot the distribution of latency and snr.

from Network import *
from Connection import *
import matplotlib.pyplot as plt
import random  # this is useful to generate random combination of nodes

Net2 = Network()  # object of Network
Net2.connect()  # recall connect to create the Network
# Net2.draw()  # draw the Network
Net2.weighted_paths_dataframe()  # recall weighted_paths to calculate the latency and snr of paths

node_list = list(Net2.nodes.keys())  # the elements of dictionary "nodes" are taken and insert in a list "node_list"
connection_obj_list = []  # list of instances of class connection
given_data = {}  # data given to the class connection -> dictionary
signal_power = 1  # signal_power equal to 1mW

latency_list = []
snr_list = []

# Now I have to create 100 connections, and then I can use the method "stream" to find latency and snr
for i in range(100):
    tmp = random.sample(node_list, 2)  # It means -> from node_list rake two random values
    given_data["input"] = tmp[0]  # define the attributes of connection object...
    given_data["output"] = tmp[1]
    given_data["signal_power"] = signal_power

    objConnection = Connection(given_data)  # ...and now create the object with that attributes
    connection_obj_list.append(objConnection)  # Now the list of instances for 100 connection is created!

# Now I use the "stream" method to calculate the best latency and snr for all the 100 instances
Net2.stream(connection_obj_list, signal_power, key="latency")
for conn in connection_obj_list:
    latency_list.append(conn.latency)

Net2.stream(connection_obj_list, signal_power, key="snr")
for conn in connection_obj_list:
    if conn.snr != 0:
        snr_list.append(conn.snr)

plt.figure()
plt.hist(latency_list)
plt.xlabel("Latency [s]")
plt.ylabel("Number of times")
plt.title("Distribution of the latency")

plt.figure()
plt.hist(snr_list)
plt.xlabel("snr [dB]")
plt.ylabel("Number of times")
plt.title("Distribution of the Signal_to_Noise Ratio (SNR)")

plt.show()
