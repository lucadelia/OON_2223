class Node:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._position = in_dict['position']
        self._connected_nodes = in_dict ['connected_nodes']
        self._successive = {}   # inizializzato dizionario vuoto

        # Si definiscono tutti i GETTER
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

        # Si definiscono tutti i SETTER
        @label.setter
        def label(self, label_value):
            self._label = label_value

        @noise_power.setter
        def position(self, position_value):
            self._position = position_value

        @latency.setter
        def connected_nodes(self, conn_nodes):
            self._connected_nodes = conn_nodes

        @path.setter
        def successive(self, succ):
            self._successive = succ

        # XXXXXXXXXXXXXXXXXXXXXXXXXX
        # Manca Metodo