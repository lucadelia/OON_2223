from core.Signal_information import *
from core.Constant_definition import *


# EXTENSION of the class Signal_information, accept the same input but also "channel" that is useful to define the
# frequency slot the signal occupies when is propagated.

class Lightpath(SignalInformation):
    def __init__(self, signal_power, path, channel):
        SignalInformation.__init__(self, signal_power, path)
        self._channel = channel
        self._rs = rs
        self._df = df

    @property
    def channel(self):
        return self._channel

    @property
    def rs(self):
        return self._rs

    @property
    def df(self):
        return self._df

    # SETTER -----------------------------------------------------------------------------------------------------------

    @channel.setter
    def channel(self, value):
        self._channel = value

    @rs.setter
    def rs(self, value):
        self._rs = value

    @df.setter
    def df(self, value):
        self._df = value
