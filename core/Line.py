import Signal_information

class Line:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._length = in_dict['position']
        self._successive = {}

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

        # SETTER -------------------------------------------------------------------------------------------------------
        @label.setter
        def label(self, value):
            self._label = value

        @length.setter
        def length(self, value):
            self._lenght = value

        @successive.setter
        def successive(self, value):
            self._successive = value

        # A line introduce some LATENCY and some NOISE, we need to add this error to the signal-------------------------
        def latency_generation(self):
            c = 299792458
            latency = self._length / ((2/3)*c)  # latency added to the signal due the line.
            return latency

        def noise_generation(self, signal_power):
            noise = 1**(-9) * signal_power * self._length
            return noise

        # Define a propagate method that update the signal information and call the successive element propagate method.
        def propagate (self, signal_information):

            # LATENCY
            latency = self.latency_generation()             # the latency is calculated inside the function. Nothing must be passed to this function.
            signal_information.update_latency(latency)      # finally we update the latency of the signal, due to the parameters of the line (depends
                                                            # on the length).
            # NOISE
            signal_power = signal_information.signal_power  # we take the value of the power of the signal.
            noise = self.noise_generation(signal_power)     # we pass this value to the function to add the noise of the line.
            signal_information.update_noise_power(noise)    # finally we update the value of the signal now considering the noise!

            line_node = self.successive[signal_information.path[0]]         # the first node of the path of the signal is stored thanks to the "successive" method
                                                                            # so the first node of the line is defined.
            signal_information = line_node.propagate(signal_information)    # Ricorsivity of the function "propagate", return the value passed
            return signal_information
