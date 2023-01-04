import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from Node import *  # All methods and attributes are included here, methods will be used
from Line import *  # same thing for Line class
from Signal_information import *


class Network:
    def __init__(self, json_file):
        self._nodes = {}  # empty dict of nodes initialized
        self._lines = {}  # empty dict for lines
        self._weighted_path = None  # Is asked that weighted_path must be an attribute for this class (Dataframe)
        self._probe = None
        self._route_space = None
        self._data_dict = None      # Take the data from the json file

        # FIRST: CONSTRUCTOR -> read the json (our network) and save all the parameters and give them to the classes----

        with open(json_file, 'r') as read:  # the file that is passed to this class is read...
            self.data_dict = json.load(read)  # ...and save the variable in a dictionary (must specify the path)

        # Now dictionary for Node and Line must be set
        node_dict = {}
        line_dict = {}

        for actual_node in self.data_dict:
            node_dict['label'] = actual_node  # the json file have (first of all) the label of all nodes, so I save this
            node_dict['connected_nodes'] = self.data_dict[actual_node]['connected_nodes']
            node_dict['position'] = self.data_dict[actual_node]['position']  # In the json there are this keywords
            self._nodes[actual_node] = Node(node_dict)
            # The json is scanned. The name of the Nodes, nodes that are connected and their position are saved.
            # This information is saved in the node_dict{} dictionary. So, when the object of the class Network
            # is called at a specific position, that node is saved recalling the class node by passing the node_dict.
            # The class "Node" accept a dictionary in input that want the label, connected nodes and position.

            # Now the LINE is described. The "Line" class accept a dictionary with label and position.
            # The label is the direction of connection of nodes like AB, BC, ... So I need to glue the actual node
            # (node_pointer) with the nodes "connected_nodes"
            for node_connected in node_dict['connected_nodes']:
                line_label = actual_node + node_connected

                # actual_node = A ; node_connected = B (where B is a possible node connected to A and the first of the
                # "connected_nodes" list) -> the name of the line is AB

                # The class line accept also a position value (his length)
                position_1 = np.array(self.data_dict[actual_node]['position'])  # explicit with data_dict for same indent
                position_2 = np.array(self.data_dict[node_connected]['position'])
                line_length = np.linalg.norm(position_1 - position_2)  # numpy method that calculate the distance

                line_dict["label"] = line_label  # the line XY is saved in the line dictionary
                line_dict["length"] = line_length  # same for the length
                self._lines[line_label] = Line(line_dict)  # I give the dictionary to the "Line" class defined by label

    # SECOND: Setter and Getter-----------------------------------------------------------------------------------------
    @property
    def nodes(self):
        return self._nodes

    @property
    def lines(self):
        return self._lines

    @property
    def weighted_path(self):
        return self._weighted_path

    @property
    def data_dict(self):
        return self._data_dict

    @property
    def probe(self):
        return self._probe

    @property
    def route_space(self):
        return self._route_space

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @lines.setter
    def lines(self, value):
        self._lines = value

    @weighted_path.setter
    def weighted_path(self, value):
        self._weighted_path = value

    @data_dict.setter
    def data_dict(self, value):
        self._data_dict = value

    @probe.setter
    def probe(self, value):
        self._probe = value

    @route_space.setter
    def route_space(self, value):
        self._route_space = value

    # THIRD: define the method "connect"--------------------------------------------------------------------------------
    def connect(self):
        for actual_node in self.nodes:
            self.nodes[actual_node].switching_matrix = {}   # empty dict for each node
            for node_connected in self.nodes[actual_node].connected_nodes:
                line_label = actual_node + node_connected
                self.nodes[actual_node].successive[line_label] = self.lines[line_label]  # nodes attached line
                self.lines[line_label].successive[node_connected] = self.nodes[node_connected]  # lines attached nodes
                self.nodes[actual_node].switching_matrix[node_connected] = self.data_dict[actual_node]['switching_matrix'][node_connected]

                ''' # Initialization of the Switching Matrix -> LAB 6
                switching_matrix_dict = {}
                for out_node_conn in self.nodes[actual_node].connected_nodes:
                    if node_connected == out_node_conn:
                        # array filled with zeros of type int
                        switching_matrix_dict[out_node_conn] = np.zeros(N_channel).astype(int)
                    else:
                        # array filled with ones of type int
                        switching_matrix_dict[out_node_conn] = np.ones(N_channel).astype(int)
                # fill the dict inside the dict (the connected nodes)
                self.nodes[actual_node].switching_matrix[node_connected] = switching_matrix_dict
                '''

    #   the "connect" method must connect the element lines and node (node needs dict of lines and vice-versa), so the
    #   "successive" method is called that update the line and the node (from the JSON).

    # FOURTH: find_path -> given two node labels, returning all path that connect them as a list of label.--------------
    # The path have to cross nodes at least once.
    def find_path(self, start_node, stop_node):
        path = ""
        path_list = []

        # Method that find all different path
        def find_next_node(actual_node, end_node, s_path):
            s_path += actual_node.label  # fill s_path string
            for current_node_analysis in actual_node.connected_nodes:  # study the connected nodes, needed for all nodes
                if current_node_analysis == end_node:
                    path_list.append(s_path + current_node_analysis)  # the path ends
                elif current_node_analysis not in s_path:  # ATTENTION: this verifies that a node is crossed only once!
                    find_next_node(self.nodes[current_node_analysis], end_node, s_path)  # restart but with new node

        # Control -> Start node = stop node
        if start_node != stop_node:
            find_next_node(self.nodes[start_node], stop_node, path)
            return path_list
        else:
            return start_node

    # FIFTH: propagate -> propagate the signal_information through the path specified and modified the information------
    def propagate(self, signal_information):
        start_node = signal_information.path[0]
        self.nodes[start_node].propagate(signal_information, None)
        return signal_information

    def propagate_probe(self, signal_information):
        start_node = signal_information.path[0]
        self.nodes[start_node].propagate_probe(signal_information)
        return signal_information

    # SIXTH: Draw -> draw the network with matplotlib-------------------------------------------------------------------
    def draw(self):
        plt.figure()  # create a new figure
        plt.grid()
        plt.xlabel("Coordinates X")
        plt.ylabel("Coordinates Y")
        plt.title("Map of the Network")
        for node_to_plot in self.nodes:
            x_coord = self.nodes[node_to_plot].position[0] * 1e-3  # On the .json the position is "1e3"
            y_coord = self.nodes[node_to_plot].position[1] * 1e-3
            plt.plot(x_coord, y_coord, "o", label=node_to_plot)  # Command legend() take node labels reporting legend
        for line_to_plot in self.lines:
            x_line1 = self.nodes[line_to_plot[0]].position[0] * 1e-3
            y_line1 = self.nodes[line_to_plot[1]].position[0] * 1e-3
            x_line2 = self.nodes[line_to_plot[0]].position[1] * 1e-3
            y_line2 = self.nodes[line_to_plot[1]].position[1] * 1e-3
            plt.plot([x_line1, y_line1], [x_line2, y_line2])
        plt.legend()
        plt.show()

    # Creates PANDAS Dataframe that contains the path string with accumulated latency, noise and SNR.-------------------
    def weighted_paths_dataframe(self):
        data = {"path": [], "noise": [], "latency": [], "snr": []}  # SET -> collection unordered
        # Now I want to find all path and I had already described find_path that accept the star_node and the stop_node
        # so to find all the combination we give to this function all the nodes thanks to the for loop:
        for start_node in self.nodes:
            for stop_node in self.nodes:
                # Two "for" to compute all the combinations of nodes
                if start_node != stop_node:
                    path_list = self.find_path(start_node, stop_node)
                    for path in path_list:
                        signal = SignalInformation(1e-3, list(path))  # OBJECT signal created with power and path
                        signal_modified = self.propagate(signal)  # The method "propagate" are called: propagate(class
                        # network) -> propagate (class Node) -> propagate (class Line). The command "list" transform the
                        # path in a list.
                        path_arrows = ""
                        for index_node in path:
                            path_arrows += index_node + "->"
                            # then "path_arrows" must be reset for the next index, useful only for representation
                        path_arrows = path_arrows[:-2]  # remove the last two indexes
                        # Now the database must be created:
                        data["path"].append(path_arrows)
                        data["noise"].append(signal_modified.noise_power)
                        data["latency"].append(signal_modified.latency)
                        snr = 10 * np.log10(signal_modified.signal_power / signal_modified.noise_power)
                        data["snr"].append(snr)
        self.weighted_path = pd.DataFrame(data)  # I have to pass to dataframe a dictionary "data" that contains list of
        # pd.set_option('display.max_rows', None)   # With this I can see the complete Dataframe
        print(self.weighted_path)  # datas like path, noise, latency ecc....

    # PROBE method to propagate the signal without the occupation of the channel
    def probe_dataframe(self):
        data = {"path": [], "noise": [], "latency": [], "snr": []}
        for start_node in self.nodes:
            for stop_node in self.nodes:
                if start_node != stop_node:
                    path_list = self.find_path(start_node, stop_node)
                    for path in path_list:
                        signal = SignalInformation(1e-3, list(path))
                        signal_modified = self.propagate_probe(signal)
                        path_arrows = ""
                        for index_node in path:
                            path_arrows += index_node + "->"
                        path_arrows = path_arrows[:-2]
                        data["path"].append(path_arrows)
                        data["noise"].append(signal_modified.noise_power)
                        data["latency"].append(signal_modified.latency)
                        snr = 10 * np.log10(signal_modified.signal_power / signal_modified.noise_power)
                        data["snr"].append(snr)
        self.probe = pd.DataFrame(data)
        # pd.set_option('display.max_rows', None)
        # print(self.probe)

    # Creates PANDAS Dataframe that describe the availability for each channel -----------------------------------------
    def route_space_dataframe(self):
        database_dict = {"path": []}    # path list
        for channel in range(N_channel):
            database_dict["CH_"+str(channel)] = []  # list of channel availability for all channel

        for start_node in self.nodes:
            for stop_node in self.nodes:
                if start_node != stop_node:
                    path_list = self.find_path(start_node, stop_node)
                    for path in path_list:
                        path_arrows = ""
                        for index_node in path:
                            path_arrows += index_node + "->"
                        path_arrows = path_arrows[:-2]      # Delete the last "->"

                        database_dict['path'].append(path_arrows)
                        for channel in range(N_channel):
                            database_dict["CH_"+str(channel)].append(0)     # '0' means occupied
        self.route_space = pd.DataFrame(database_dict)
        # pd.set_option('display.max_rows', None)
        # print(self.route_space)

    # ROUTE SPACE ------------------------------------------------------------------------------------------------------
    def route_space_update(self):
        index_range = self.route_space.index    # Save the indexes of the route space dataframe (349 paths)
        for i in index_range:
            tmp = np.ones(N_channel).astype(int)
            node_list = self.route_space['path'][i].split("->")

            for j in range(len(node_list)-1):   # exclude last node
                line_label = node_list[j] + node_list[j+1]
                tmp *= self.lines[line_label].state     # Verifies the availability of the line and do the product tmp

                if j != 0:  # exclude first node because input
                    tmp *= self.nodes[node_list[j]].switching_matrix[node_list[j-1]][node_list[j+1]]
                    # (How defined in the connect method, the state is initialized to 1, otherwise is 0)
                    # Switching matrix represent the availability to connect the nodes while the state is the
                    # availability of the channel. First the product with the state, and then with the matrix.
                    # Modify the "state" to occupy the path

            for z in range(N_channel):
                self.route_space.loc[i, 'CH_'+str(z)] = tmp[z]
        # pd.set_option('display.max_rows', None)
        # print(self.route_space)

    # FIND BEST SNR: Given two nodes, find the path with the best SNR value---------------------------------------------
    def find_best_snr(self, start_node, stop_node, channel):
        max_snr = min(self.weighted_path['snr'].values)  # with "values" I take the values of snr in the dataframe
        new_best_path = ""  # and with "min" I take the TOTAL min value of snr of dataframe

        for i, row in self.weighted_path.iterrows():
            # "iterrows" take the column specified and with "row" I can cycle the line. "iterrows" method generates an
            # iterator object of the DataFrame, allowing us to iterate each row in the DataFrame.
            if row['path'][0] == start_node and row['path'][-1] == stop_node and row['snr'] > max_snr:
                # I take the "path" column and with "row" I cycle the line.'0' and '-1' represent the first position and
                # the last position of the path in the line indicated by "row" for ex. A->B->C I have [0]=A and [-1]=C
                lightpath_available = True
                path = list(row['path'].split('->'))    # "split" uses -> like a flag to create different strings
                                                        # example: A->B->C->D became ABCD
                for j in range(len(path)-1):
                    line_label = path[j] + path[j+1]
                    if self.lines[line_label].state[channel] == 0:
                        lightpath_available = False

                if lightpath_available:
                    max_snr = self.weighted_path['snr'][i]
                    new_best_path = self.weighted_path['path'][i]
        # print("Best SNR path: " + new_best_path)
        return new_best_path

    # FIND BEST LATENCY-------------------------------------------------------------------------------------------------
    # The comment for this section are the same from above
    def find_best_latency(self, start_node, stop_node, channel):
        min_lat = max(self.weighted_path['latency'].values)
        new_best_path = ""

        # I save the max latency of the dataframe, and then I cycle all the latencies for all path to find the min one.
        for i, row in self.weighted_path.iterrows():
            if row['path'][0] == start_node and row['path'][-1] == stop_node and row['latency'] < min_lat:
                lightpath_available = True
                path = list(row['path'].split('->'))

                for j in range(len(path)-1):
                    line_label = path[j] + path[j+1]
                    if self.lines[line_label].state[channel] == 0:
                        lightpath_available = False

                if lightpath_available:     # Simplified version, same as: "if lightpath_available == True"
                    min_lat = self.weighted_path['latency'][i]
                    new_best_path = self.weighted_path['path'][i]
        # print("Best latency path: " + new_best_path)
        return new_best_path

    # STREAM METHOD -> for each element of a given list of instances of the class connection, sets lat and snr.---------
    # This will be calculated by propagating a SignalInformation object
    # connection_list is a list of instances (=object) of class Connection
    def stream(self, connection_list, signal_power, key="latency"):  # latency set to default
        for connection in connection_list:  # with "connection" I cycle all the instances...
            path = ""
            channel = -1
            if key == "latency":  # ...if the name latency is passed...
                while path == "" and channel <= N_channel-2:
                    channel += 1
                    path = self.find_best_latency(connection.input, connection.output, channel)
                    # ...the latency is taken using the attributes of the class.
            elif key == "snr":
                while path == "" and channel <= N_channel-2:
                    channel += 1
                    path = self.find_best_snr(connection.input, connection.output, channel)

            if path == "":
                connection.latency = 0
                connection.snr = 0
            else:
                # path_arrows = path
                path = path.split("->")
                signal_lightpath = Lightpath(signal_power, list(path), channel)
                final_signal = self.propagate(signal_lightpath)

                # Update of route_space
                # self._route_space.loc[self._route_space.path == path_arrows, 'CH_'+str(channel)] = 1
                # With 'loc' I decide to show only the column "path", then set the channel that is crossed available '1'

                connection.signal_power = final_signal.signal_power
                connection.latency = final_signal.latency
                connection.snr = 10 * np.log10(final_signal.signal_power / final_signal.noise_power)
                self.route_space_update()

        # Initial switching matrix restored after the streaming
        for actual_node in self.nodes:
            for node_connected in self.nodes[actual_node].connected_nodes:
                self.nodes[actual_node].switching_matrix[node_connected] = self.data_dict[actual_node]['switching_matrix'][node_connected]


