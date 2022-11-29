import numpy as np
import matplotlib.pyplot as plt
import json
#  import pandas as pd
from Node import *  # All methods and attributes are included here, methods will be used
from Line import *  # same thing for Line class


class Network:
    def __init__(self):
        self._nodes = {}  # empty dict of nodes initialized
        self._lines = {}  # empty dict for lines

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

    @nodes.setter
    def nodes(self, value):
        self._nodes = value

    @lines.setter
    def lines(self, value):
        self._lines = value

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
        def find_next_node(actual_node, stop_node, path):   # ERROR: but I need this configuration
            path += actual_node.label  # fill path string
            for current_node_analysis in actual_node.connected_nodes:  # study the connected nodes, needed for all nodes
                if current_node_analysis == stop_node:
                    path_list.append(path + current_node_analysis)  # the path ends
                elif current_node_analysis not in path:  # ATTENTION: this verifies that a node is crossed only once!
                    find_next_node(self.nodes[current_node_analysis], stop_node, path)  # restart but with the new node

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
        plt.figure()    # create a new figure
        plt.grid()
        plt.xlabel("Coordinates X")
        plt.ylabel("Coordinates Y")
        plt.title("Map of the Network")
        for node_to_plot in self.nodes:
            x_coord = self.nodes[node_to_plot].position[0]*1e-3  # On the .json the position is "1e3"
            y_coord = self.nodes[node_to_plot].position[1]*1e-3
            plt.plot(x_coord, y_coord, "o", label=node_to_plot)  # Command legend() take node labels reporting legend
        for line_to_plot in self.lines:
            x_line1 = self.nodes[line_to_plot[0]].position[0]*1e-3
            y_line1 = self.nodes[line_to_plot[1]].position[0]*1e-3
            x_line2 = self.nodes[line_to_plot[0]].position[1]*1e-3
            y_line2 = self.nodes[line_to_plot[1]].position[1]*1e-3
            plt.plot([x_line1, y_line1], [x_line2, y_line2])
        plt.legend()
        plt.show()


# EXAMPLE OF MAIN -> Write all the possible path:
# object_Net1 = Network()
# tmp = object_Net1.find_path("A", "D")
# print(tmp)

# EXAMPLE OF MAIN -> Show the plot of the Network in exam
# object_Net1 = Network()
# tmp = object_Net1.draw()
