import numpy as np
from scipy import signal
import matplotlib.pyplot as plt
from scipy.io.wavfile import write

sampling_frequency = 8000
nf = 2 * sampling_frequency
Fo = 120 #male frequency voice
T = 2
formants = np.array([800, 1200, 2500])  # Formant frequencies (F1, F2, F3)
bandwidths = np.array([70, 110, 160])  # Bandwidths for each formant
t = np.arange(0, T, 1/sampling_frequency)
source = np.zeros_like(t)

#source filter model, source will represent the glottis
#creating a source
for n in range(1, int(sampling_frequency / (2*Fo))):
        harmonic_freq = n * Fo
        source += np.cos(2*np.pi*harmonic_freq*t)
source /= np.max(np.abs(source))

#applying a filter to emphasize the vowels
vowel_sound = source 
for f, bw in zip(formants, bandwidths):
        b,a = signal.iirfilter(2, [f-bw/2, f+bw/2], analog = False, ftype = 'butter', output = 'ba', fs = sampling_frequency)
        vowel_sound = signal.lfilter(b,a,vowel_sound)
        
#applying an envelope
vowel_sound *= signal.hanning(len(t))    
vowel_sound /= np.max(np.abs(vowel_sound))

output_file = r'C:\Users\HOME\Desktop\DSA\vowel_sound.wav'
write(output_file, sampling_frequency, vowel_sound.astype(np.float32))
fig, axs = plt.subplots(2,1,figsize=(12, 4))
axs[0].plot(t, vowel_sound, label='Synthesized Vowel', color = 'r')
axs[0].set_title('Time Domain Representation of the Synthesized Vowel')
axs[0].set_xlabel('Time [s]')
axs[0].set_ylabel('Amplitude')
axs[0].legend()
axs[1].specgram(vowel_sound, Fs = sampling_frequency, cmap = 'jet')
axs[1].set_title('Spectrogram of the signal')
axs[1].set_xlabel('Time[s]')
axs[1].set_ylabel('Frequency')
axs[1].legend()
plt.tight_layout()
plt.show()

