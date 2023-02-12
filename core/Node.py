from Line import *


class Node:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._position = in_dict['position']
        self._connected_nodes = in_dict['connected_nodes']
        self._successive = {}  # initialized dictionary to zero (empty)
        self._switching_matrix = None
        self._transceiver = in_dict['transceiver']

    # GETTER -------------------------------------------------------------------------------------------------------
    @property
    def label(self):
        return self._label

    @property
    def position(self):
        return self._position

    @property
    def connected_nodes(self):
        return self._connected_nodes

    @property
    def successive(self):
        return self._successive

    @property
    def switching_matrix(self):
        return self._switching_matrix

    @property
    def transceiver(self):
        return self._transceiver

    # SETTER -------------------------------------------------------------------------------------------------------
    @label.setter
    def label(self, value):
        self._label = value

    @position.setter
    def position(self, value):
        self._position = value

    @connected_nodes.setter
    def connected_nodes(self, value):
        self._connected_nodes = value

    @successive.setter
    def successive(self, value):
        self._successive = value

    @switching_matrix.setter
    def switching_matrix(self, value):
        self._switching_matrix = value

    @transceiver.setter
    def transceiver(self, value):
        self._transceiver = value

    # Define a propagate method that update a signal_information object modifying its path -----------------------------
    # attribute and call the successive one.

    def propagate(self, signal_information, prev_node):  # prev_node is given from label[0] of class Line
        signal_information.update_path()
        if len(signal_information.path) != 0:  # condition to break the recursivity -> we want at least 2 elements
            if isinstance(signal_information, Lightpath) and prev_node is not None:
                # None is an initialization that is valid only for the first time, then is = label[0]
                # If the signal is propagated then the channel will be occupied
                self.switching_matrix[prev_node][signal_information.path[0]][signal_information.channel] = 0
                # then the channel is updated, so I have to block the previous and the next channels
                # a verification is seen for the first and last channel that obv don't have prev and next channels.
                # Unless they are...
                if signal_information.channel != 0:
                    self.switching_matrix[prev_node][signal_information.path[0]][signal_information.channel-1] = 0
                if signal_information.channel != N_channel-1:
                    self.switching_matrix[prev_node][signal_information.path[0]][signal_information.channel+1] = 0

            next_line = self.label + signal_information.path[0]
            signal_information.signal_power = self.successive[next_line].optimized_launch_power()
            # "optimized_launch_power()" set the optimal launch power for each line
            self.successive[next_line].propagate(signal_information)
        return signal_information

    # ------------------------------------------------------------------------------------------------------------------
    def propagate_probe(self, signal_information):
        signal_information.update_path()
        if len(signal_information.path) != 0:
            next_line = self.label + signal_information.path[0]
            self.successive[next_line].propagate_probe(signal_information)
        return signal_information
