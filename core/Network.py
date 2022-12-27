import numpy as np
import matplotlib.pyplot as plt
import json
import pandas as pd
from Node import *  # All methods and attributes are included here, methods will be used
from Line import *  # same thing for Line class
from Signal_information import *


class Network:
    def __init__(self):
        self._nodes = {}  # empty dict of nodes initialized
        self._lines = {}  # empty dict for lines
        self._weighted_path = 0  # Is asked that weighted_path must be an attribute for this class

        # FIRST: CONSTRUCTOR -> read the json (our network) and save all the parameters and give them to the classes----

        with open("nodes.json", 'r') as read:  # the file that is passed to this class is read...
            data_dict = json.load(read)  # ...and save the variable in a dictionary

        # Now dictionary for Node and Line must be set
        node_dict = {}
        line_dict = {}

        for actual_node in data_dict:
            node_dict['label'] = actual_node  # the json file have (first of all) the label of all nodes, so I save this
            node_dict['connected_nodes'] = data_dict[actual_node]['connected_nodes']
            node_dict['position'] = data_dict[actual_node]['position']  # In the json there are this keywords
            self._nodes[actual_node] = Node(node_dict)
            # The json is scanned. The name of the Nodes, nodes that are connected and their position are saved.
            # This information is saved in the node_dict{} dictionary. So, when the object of the class Network
            # is called at a specific position, that node is saved recalling the class node by passing the node_dict.
            # The class "Node" accept a dictionary in input that want the label, connected nodes and position.

            # Now the LINE is described. The "Line" class accept a dictionary with label and position.
            # The label is the direction of connection of nodes like AB, BC, ... So I need to glue the actual node
            # (node_pointer) with the nodes "connected_nodes"
            for node_connected in node_dict["connected_nodes"]:
                line_label = actual_node + node_connected

                # actual_node = A ; node_connected = B (where B is a possible node connected to A and the first of the
                # "connected_nodes" list) -> the name of the line is AB

                # The class line accept also a position value (his length)
                position_1 = np.array(data_dict[actual_node]['position'])  # explicit with data_dict for same indent
                position_2 = np.array(data_dict[node_connected]['position'])
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

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @lines.setter
    def lines(self, value):
        self._lines = value

    @weighted_path.setter
    def weighted_path(self, value):
        self._weighted_path = value

    # THIRD: define the method "connect"--------------------------------------------------------------------------------
    def connect(self):
        for actual_node in self.nodes:
            for node_connected in self.nodes[actual_node].connected_nodes:
                line_label = actual_node + node_connected
                self.nodes[actual_node].successive[line_label] = self.lines[line_label]  # nodes attached line
                self.lines[line_label].successive[node_connected] = self.nodes[node_connected]  # lines attached nodes

    #   the "connect" method must connect the element lines and node (node needs dict of lines and vice-versa), so the
    #   "successive" method is called that update the line and the node.

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
        self.nodes[start_node].propagate(signal_information)
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

    # LAB 2: Creates PANDAS Dataframe that contains the path string with accumulated latency, noise and SNR.------------

    def weighted_paths_dataframe(self):
        data = {"path": [], "noise": [], "latency": [], "snr": []}  # SET -> collection unordered
        # Now I want to find all path and I had already described find_path that accept the star_node and the stop_node
        # so to find all the combination we give to this function all the nodes thanks to the for loop:
        self.connect()
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
        print(self.weighted_path)  # datas like path, noise, latency ecc....

    # FIND BEST SNR: Given two nodes, find the path with the best SNR value---------------------------------------------
    def find_best_snr(self, start_node, stop_node):
        max_snr = min(self.weighted_path['snr'].values)  # with "values" I take the values of snr in the dataframe
        new_best_path = ""  # and with "min" I take the TOTAL min value of snr of dataframe

        for i, row in self.weighted_path.iterrows():
            # "iterrows" take the column specified and with "row" I can cycle the line. "iterrows" method generates an
            # iterator object of the DataFrame, allowing us to iterate each row in the DataFrame.
            if row['path'][0] == start_node and row['path'][-1] == stop_node and row['snr'] > max_snr:
                # I take the "path" column and with "row" I cycle the line.'0' and '-1' represent the first position and
                # the last position of the path in the line indicated by "row" for ex. A->B->C I have [0]=A and [-1]=C
                path = list(row['path'].split('->'))    # "split" uses -> like a flag to create different strings
                                                        # example: A->B->C->D became ABCD
                max_snr = self.weighted_path['snr'][i]
                new_best_path = self.weighted_path['path'][i]
        # print(new_best_path)
        return new_best_path

    # FIND BEST LATENCY-------------------------------------------------------------------------------------------------
    # The comment for this section are the same from above
    def find_best_latency(self, start_node, stop_node):
        min_lat = max(self.weighted_path['latency'].values)
        new_best_path = ""
        # I save the max latency of the dataframe, and then I cycle all the latencies for all path to find the min one.
        for i, row in self.weighted_path.iterrows():
            if row['path'][0] == start_node and row['path'][-1] == stop_node and row['latency'] < min_lat:
                path = list(row['path'].split('->'))
                min_lat = self.weighted_path['latency'][i]
                new_best_path = self.weighted_path['path'][i]
        # print(new_best_path)
        return new_best_path

    # STREAM METHOD -> for each element of a given list of instances of the class connection, sets lat and snr.---------
    # This will be calculated by propagating a SignalInformation object
    def stream(self, connection_list, signal_power, key="latency"):  # latency set to default
        # connection_list is a list of instances (=object) of class Connection
        for connection in connection_list:  # with "connection" I cycle all the instances...
            path = ""
            if key == "latency":  # ...if the name latency is passed...
                while path == "":
                    path = self.find_best_latency(connection.input, connection.output)  # ...the latency is taken using
            elif key == "snr":                                                          # the attributes of the class.
                while path == "":
                    path = self.find_best_snr(connection.input, connection.output)

            if path == "":
                connection.latency = 0
                connection.snr = 0
            else:
                path = path.split("->")
                signal = SignalInformation(signal_power, list(path))
                final_signal = self.propagate(signal)

                connection.signal_power = final_signal.signal_power
                connection.latency = final_signal.latency
                connection.snr = 10 * np.log10(final_signal.signal_power / final_signal.latency)


