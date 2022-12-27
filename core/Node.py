class Node:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._position = in_dict['position']
        self._connected_nodes = in_dict['connected_nodes']
        self._successive = {}  # initialized dictionary to zero (empty)

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

    # Define a propagate method that update a signal_information object modifying its path -------------------------
    # attribute and call the successive one.

    def propagate(self, signal_information):  # node.propagate(signal_information) begin "propagate" for the node.
        signal_information.update_path()    # recall the update of the path of signal_inf
        if len(signal_information.path) != 0:  # condition to break the recursivity -> we want at least 2 elements
            next_line = self.label + signal_information.path[0]
            self.successive[next_line].propagate(signal_information)
        return signal_information
