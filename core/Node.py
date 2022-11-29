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

    def propagate(self, signal_information):  # node.propagate(signal_information) begin "propagate" for the node
        actual_path = signal_information.path  # saves actual path of the signal_inf in the variable "actual_path"
        if len(actual_path) > 1:  # condition to break the recursivity -> we want at least 2 elements
            line_name = actual_path[:2]  # line_name contains line path (composed by 2 elements: AB for ex.)
            line = self.successive[line_name]  # the successive node is set
            signal_information.update_path()  # the signal_inf. object update his path (method of sign_inf class)
            signal_information = line.propagate(signal_information)  # call to this recursive method
        return signal_information
