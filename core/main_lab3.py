from Network import *
from Signal_information import *

Net1 = Network()

data = {"path": [], "noise": [], "latency": [], "SNR": []}  # SET -> collection unordered
# Now I want to find all path and I had already described find_path that accept the star_node and the stop_node
# so to find all the combination we give to this function all the nodes thanks to the for loop:
Net1.connect()
for start_node in Net1.nodes:
    for stop_node in Net1.nodes:
        # Two "for" to compute all the combinations of nodes
        if start_node != stop_node:
            path_list = Net1.find_path(start_node, stop_node)
            for path in path_list:
                signal = SignalInformation(1e-3, list(path))  # OBJECT signal created with power and path
                signal_modified = Net1.propagate(signal)  # The method "propagate" are called: propagate(class
                # network) -> propagate (class Node) -> propagate (class Line). The command "list" transform the
                # path in a list.
                path_arrows = " "
                for index_node in path:
                    path_arrows += index_node + "->"
                    # then "path_arrows" must be reset for the next index, useful only for representation
                path_arrows = path_arrows[:-2]  # remove the last two indexes
                # Now the database must be created:
                data["path"].append(path_arrows)
                data["noise"].append(signal_modified.noise_power)
                data["latency"].append(signal_modified.latency)
                snr = 10 * np.log10(signal_modified.signal_power / signal_modified.noise_power)
                data["SNR"].append(snr)
                Net1.weighted_path = pd.DataFrame(data)
# print(Net1.weighted_path)

# Here follow some test that I made during the project: (Not requested)

# EXAMPLE OF MAIN -> Write all the possible path:
object_Net0 = Network()
tmp = object_Net0.find_path("A", "D")
print(tmp)

# EXAMPLE OF MAIN -> Show the plot of the Network in exam
object_Net1 = Network()
tmp = object_Net1.draw()

# EXAMPLE OF MAIN -> Return the  best SNR and the LATENCY
object_Net2 = Network()
object_Net2.weighted_paths_dataframe()
print(object_Net2.find_best_snr('A', 'B'))
print(object_Net2.find_best_latency('A', 'B'))

