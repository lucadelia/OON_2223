from scipy.constants import h       # Plank constant [J*s]
from scipy.constants import pi
from scipy import special
# Numpy function, is a library that contain the function "erfcinv" -> inverse of the complementary error function
import numpy as np

N_channel = 10

bn = 12.5e9             # Noise bandwidth [Hz]
BERt = 1e-3             # Bit error rate (BER)
rs = 32e9               # Symbol rate [baud/s][Hz] -> [GHz]
df = 50e9               # frequency spacing between two consecutive channels [Hz] -> [GHz]

amp_gain = 16           # Gain of the amplifier [dB]
amp_nf = 5.5            # Noise figure [dB]
freq = 193.414e12       # frequency centered in C-band [Hz]

alpha = 0.2             # [dB/km]
beta2 = 2.13e-26        # [ps^2/km]
gamma = 1.27e-3         # [m*W^-1]
e = np.exp(1)

# Functions
alpha_lin = alpha*1e-3/(20*np.log10(e))
nf = 10 ** (amp_nf / 10)
gain = 10 ** (amp_gain / 10)
l_eff = 1/2*alpha_lin
