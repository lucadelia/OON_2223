class SignalInformation:
    def __init__(self, signal_power, path):  # costruttore -> solo signal_power e path ricevono valori dall'esterno
        self._signal_power = signal_power
        self._path = path
        self._noise_power = 0    # rumore inizializzato a zero
        self._latency = 0        # latenza inizializzata a zero

        # Si definiscono tutti i GETTER (restituiscono i valori degli attributi)
        @property   # setter di signal_power
        def signal_power(self):
            return self._signal_power   # restituisce l'attributo signal_power dell'oggetto

        @property   # setter di noise_power
        def noise_power(self):
            return self._noise_power

        @property   # setter di latency
        def latency(self):
            return self._latency

        @property   # setter di path
        def path(self):
            return self._path

        # Si definiscono tutti i SETTER
        @signal_power.setter
        def signal_power(self, sp_value):
            self._signal_power = sp_value

        @noise_power.setter
        def noise_power(self, np_value):
            self._noise_power = np_value

        @latency.setter
        def latency(self, lat):
            self._latency = lat

        @path.setter
        def path(self, path):
            self._path = path

        # Si definiscono i metodi per incrementare gli attributi di una quantità fornita
        # In questo caso non si usa @property
        def increment_signal_power(self, sp_value):
            self.signal_power += sp_value

        def increment_noise_power(self, np_value):
            self.noise_power += np_value

        def increment_latency(self, lat):
            self.latency += lat

        # Manca l'aggiornamento del Path
        # XXXXXXXXXXXXXXXXXXXXXX