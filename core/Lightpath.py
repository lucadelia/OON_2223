from Signal_information import *


# EXTENSION of the class Signal_information, accept the same input but also "channel" that is useful to define the
# frequency slot the signal occupies when is propagated.

class Lightpath(SignalInformation):
    def __init__(self, signal_power, path, channel):
        SignalInformation.__init__(self, signal_power, path)
        self._channel = channel

    @property
    def channel(self):
        return self._channel

    @channel.setter
    def channel(self, value):
        self._channel = value
