import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import convolve

n = np.arange(0,6)

x = n / (2**n/2**3) #further simplified
t = np.linspace(-4,4,1000)
Ts = 1/500
def sinc_function(t, Ts):
    return (np.sin(np.pi*t/Ts)) / (np.pi*t/Ts)

# Apply the sinc function to the time range
pt = sinc_function(t, Ts)

# Define the interpolation pulses based on the provided sketches
def p_1_3a(t):
    return np.where(np.abs(t) <= 1, 1, 0)

def p_1_3b(t):
    return np.where(t <= 0, np.where(t >= -1.8, 1, 0), np.where(t <= 0.2, -5*t + 1, 0))

def p_1_3c(t):
    return np.where(t < 0, np.where(t >= -2, 0.5*t + 1, 0), np.where(t < 2, -0.5*t + 1, 0))

# Calculate the continuous-time pulses by interpolating the values between samples
p_1_3a_continuous = p_1_3a(t)
p_1_3b_continuous = p_1_3b(t)
p_1_3c_continuous = p_1_3c(t)

# Convolve the discrete sequence with each of the pulses
# Using 'full' gives the convolution at each point of overlap
y_1_3a = convolve(x, p_1_3a_continuous, mode='full')[:1000]  
y_1_3b = convolve(x, p_1_3b_continuous, mode='full')[:1000]
y_1_3c = convolve(x, p_1_3c_continuous, mode='full')[:1000]

fig, axs = plt.subplots(5,1,figsize = (18,8))
axs[0].stem(n, x, basefmt=" ", use_line_collection= True, linefmt= '-')
axs[0].set_xlabel('n')
axs[0].set_ylabel('x[n]')
axs[0].set_title('Discrete sequence x[n]')

axs[1].plot(t, pt)
axs[1].set_xlabel('Time')
axs[1].set_ylabel('P(t)')
axs[1].set_title('Pulse function plot')

# Plot the convolution with interpolation pulse 1.3a
axs[2].plot(t, y_1_3a, label='Convolution with Fig. 1.3a')
axs[2].set_title('Convolution with interpolation pulse from Fig. 1.3a')
axs[2].set_xlabel('Time (ms)')
axs[2].set_ylabel('Amplitude')


# Plot the convolution with interpolation pulse 1.3b
axs[3].plot(t, y_1_3b, label='Convolution with Fig. 1.3b', color='orange')
axs[3].set_title('Convolution with interpolation pulse from Fig. 1.3b')
axs[3].set_xlabel('Time (ms)')
axs[3].set_ylabel('Amplitude')


# Plot the convolution with interpolation pulse 1.3c
#linear interpolation 
axs[4].stem(n, x)
axs[4].set_title('Convolution with interpolation pulse from Fig. 1.3c')
axs[4].set_xlabel('Time (ms)')
axs[4].set_ylabel('Amplitude')

plt.tight_layout()
plt.show()