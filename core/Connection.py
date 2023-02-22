class Connection:
    def __init__(self, given_data):
        self._input = given_data['input']     # must be a string, so a list of one element is defined -> input
        self._output = given_data['output']   # string, same as above -> output
        self._signal_power = given_data['signal_power']   # same but float -> signal_power
        self._latency = 0   # float
        self._snr = None    # float
        self._bit_rate = 0

    @property
    def input(self):
        return self._input

    @property
    def output(self):
        return self._output

    @property
    def signal_power(self):
        return self._signal_power

    @property
    def latency(self):
        return self._latency

    @property
    def snr(self):
        return self._snr

    @property
    def bit_rate(self):
        return self._bit_rate

    # ------------------------------------------------------------------------------------------------------------------

    @signal_power.setter
    def signal_power(self, value):
        self._signal_power = value

    @latency.setter
    def latency(self, value):
        self._latency = value

    @snr.setter
    def snr(self, value):
        self._snr = value

    @bit_rate.setter
    def bit_rate(self, value):
        self._bit_rate = value
