from Lightpath import *

N_channel = 10


class Line:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._length = in_dict['length']
        self._successive = {}
        self._state = []  # Channel availability -> show if a connection is occupied. List of string (occup. channel)

        for index in range(N_channel):  # It asked to implement 10 channels for each line
            self._state.append("free")  # Initialization to "free"

    # GETTER -------------------------------------------------------------------------------------------------------
    @property
    def label(self):
        return self._label

    @property
    def length(self):
        return self._length

    @property
    def successive(self):
        return self._successive

    @property
    def state(self):
        return self._state

    # SETTER -------------------------------------------------------------------------------------------------------
    @label.setter
    def label(self, value):
        self._label = value

    @length.setter
    def length(self, value):
        self._length = value

    @successive.setter
    def successive(self, value):
        self._successive = value

    @state.setter
    def state(self, value):
        self._state = value

    # A line introduce some LATENCY and some NOISE, we need to add this error to the signal-----------------------------
    def latency_generation(self):
        c = 299792458
        latency = self._length / ((2 / 3) * c)  # latency added to the signal due the line.
        return latency

    def noise_generation(self, signal_power):
        noise = (10 ** (-9)) * signal_power * self._length
        return noise

    # Define a propagate method that update the signal information and call the successive element propagate method.
    def propagate(self, signal_information):
        # Latency
        latency = self.latency_generation()
        signal_information.update_latency(latency)

        # Noise
        signal_power = signal_information.signal_power  # we take the value of the power of the signal.
        noise = self.noise_generation(signal_power)  # we pass this value to the function to add noise of the line.
        signal_information.update_noise_power(noise)  # update the value of the signal considering the noise

        # if object is in Lightpath -> I want to take it so... -> change its state in "occupied"
        if isinstance(signal_information, Lightpath):
            self.state[signal_information.channel] = "occupied"
        signal_information = self.successive[signal_information.path[0]].propagate(signal_information)
        return signal_information

    def propagate_probe(self, signal_information):
        # Latency
        latency = self.latency_generation()
        signal_information.update_latency(latency)

        # Noise
        signal_power = signal_information.signal_power
        noise = self.noise_generation(signal_power)
        signal_information.update_noise_power(noise)

        line_node = self.successive[signal_information.path[0]]
        signal_information = line_node.propagate_probe(signal_information)
        return signal_information
