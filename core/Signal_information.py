class SignalInformation:
    def __init__(self, signal_power, path):  # constructor -> only signal_pow and path take values from the outside
        self._signal_power = signal_power
        self._path = path
        self._noise_power = 0  # noise initialized to zero
        self._latency = 0  # latency initialized to zero

    # GETTER (return the value of the attributes)-------------------------------------------------------------------
    @property  # getter of "signal_power"
    def signal_power(self):
        return self._signal_power  # return the attributes signal_power of the object

    @property  # getter of "noise_power"
    def noise_power(self):
        return self._noise_power

    @property  # getter of "latency"
    def latency(self):
        return self._latency

    @property  # getter of "path"
    def path(self):
        return self._path

    # SETTER -------------------------------------------------------------------------------------------------------
    @signal_power.setter
    def signal_power(self, value):
        self._signal_power = value

    @noise_power.setter
    def noise_power(self, value):
        self._noise_power = value

    @latency.setter
    def latency(self, value):
        self._latency = value

    @path.setter
    def path(self, value):
        self._path = value

    # defined method to update the attributes of a defined quantities ----------------------------------------------

    def update_signal_power(self, value):
        self.signal_power += value

    def update_noise_power(self, value):
        self.noise_power += value

    def update_latency(self, value):
        self.latency += value

    def update_path(self):
        self.path = self.path[1:]  # if I call this method, the path is updated and the new path stats from the
        # position '1'. The position '1' became the new position '0'. All other position
        # of the path remain stored following the newest position.
