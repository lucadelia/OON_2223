import Signal_information

class Node:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._position = in_dict['position']
        self._connected_nodes = in_dict['connected_nodes']
        self._successive = {}   # initialized dictionary to zero (empty)

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

        # SETTER -------------------------------------------------------------------------------------------------------
        @label.setter
        def label(self, label_value):
            self._label = label_value

        @position.setter
        def position(self, position_value):
            self._position = position_value

        @connected_nodes.setter
        def connected_nodes(self, conn_nodes):
            self._connected_nodes = conn_nodes

        @successive.setter
        def successive(self, succ):
            self._successive = succ

        # Define a propagate method that update a signal_information object modifying its path attribute and call the successive one

        # def propagate (self, signal_information):
        #    actual_path = signal_information.path
        #    if len(actual_path)