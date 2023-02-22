from core.Lightpath import *
from core.Constant_definition import *


class Line:
    def __init__(self, in_dict):
        self._label = in_dict['label']
        self._length = in_dict['length']
        self._successive = {}
        self._state = []  # Channel availability -> show if a connection is occupied. List of string (occup. channel)

        # Initialization of the line as FREE (so not occupied)
        self._state = np.ones(N_channel).astype(int)    # Change the availability in integers and use array

        self._n_amplifiers = np.ceil(self._length*1e-3/80)+1     # number of amplifier (one every 80 km)
        self._amp_gain = in_dict['amp_gain']
        self._amp_nf = in_dict['amp_nf']
        self._alpha = in_dict['alpha']      # [dB/km]
        self._beta2 = in_dict['beta2']      # [(m*HZ^2)^-1)]
        self._gamma = in_dict['gamma']      # [1/m*W]

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

    @property
    def n_amplifiers(self):
        return self._n_amplifiers

    @property
    def amp_gain(self):
        return self._amp_gain

    @property
    def amp_nf(self):
        return self._amp_nf

    @property
    def alpha(self):
        return self._alpha

    @property
    def beta2(self):
        return self._beta2

    @property
    def gamma(self):
        return self._gamma

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

    @n_amplifiers.setter
    def n_amplifiers(self, value):
        self._n_amplifiers = value

    @amp_gain.setter
    def amp_gain(self, value):
        self._amp_gain = value

    @amp_nf.setter
    def amp_nf(self, value):
        self._amp_nf = value

    @alpha.setter
    def alpha(self, value):
        self._alpha = value

    @beta2.setter
    def beta2(self, value):
        self._beta2 = value

    @gamma.setter
    def gamma(self, value):
        self._gamma = value

    # A line introduce some LATENCY and some NOISE, we need to add this error to the signal-----------------------------
    def latency_generation(self):
        c = 299792458
        latency = self._length / ((2 / 3) * c)  # latency added to the signal due the line.
        return latency

    def noise_generation(self, signal_power):
        ASE_noise = self.ase_generation()
        NLI_noise = self.nli_generation(signal_power)
        total_noise = ASE_noise + NLI_noise
        return total_noise

    # Define a propagate method that update the signal information and call the successive element propagate method.----
    def propagate(self, signal_information):
        # Latency
        latency = self.latency_generation()
        signal_information.update_latency(latency)

        # Noise
        signal_power = signal_information.signal_power  # we take the value of the power of the signal.
        noise = self.noise_generation(signal_power)     # we pass this value to the function to add noise of the line.
        signal_information.update_noise_power(noise)    # update the value of the signal considering the noise

        signal_information.update_inv_gsnr(noise/signal_information.signal_power)
        # (Pase + Pnli) / Pch

        # if object is in Lightpath -> I want to take it so... -> change its state in "occupied"
        if isinstance(signal_information, Lightpath):
            self.state[signal_information.channel] = 0
        signal_information = self.successive[signal_information.path[0]].propagate(signal_information, self.label[0])
        return signal_information

    # ------------------------------------------------------------------------------------------------------------------
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

    # ------------------------------------------------------------------------------------------------------------------
    def ase_generation(self):
        ase = self.n_amplifiers*h*freq*bn*nf*(gain-1)    # constant defined in "Constant_definition"
        return ase

    # ------------------------------------------------------------------------------------------------------------------
    def nli_generation(self, signal_power):
        # Evaluate the total amount of NLI generated by the non-linear interface noise
        n_span = self.n_amplifiers-1
        n_nli = (16/(27*pi))*np.log((pi*pi*self.beta2*rs*rs*N_channel**(2*rs/df))/(2*alpha_lin))*(
                self.gamma*self.gamma*alpha_lin*l_eff*l_eff)/(self.beta2*rs**3)
        NLI = signal_power ** 3 * n_nli * n_span * bn    # Non-linear interference
        return NLI

    # ------------------------------------------------------------------------------------------------------------------
    def optimized_launch_power(self):
        n_nli = (16 / (27 * pi)) * np.log(
            (pi * pi * self.beta2 * rs * rs * N_channel ** (2 * rs / df)) / (2 * alpha_lin)) * (
                            self.gamma * self.gamma * alpha_lin * l_eff * l_eff) / (self.beta2 * rs ** 3)
        ase = self.ase_generation()
        n_span = self.n_amplifiers - 1

        optimized_power = (ase/(2*n_nli*bn*n_span))**(1/3)
        return optimized_power
