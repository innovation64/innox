import numpy as np
from scipy import signal
import wave
import matplotlib.pyplot as plt

# read audio file recorded by Raspberry Pi
file = wave.open("./record.wav","rb")
# get sampling frequency
sf = file.getframerate()
# get audio data total length
nLength = file.getnframes()
# read audio data
audioDataRaw = file.readframes(nLength)
# transfer to python list
audioDataRaw = list(audioDataRaw)
# transfer to numpy array
audioDataRaw = np.asarray(audioDataRaw,np.int8)
# set the data type to int16
audioDataRaw.dtype = "int16"
# calculate audio length in second
audioDataRawTotalTime = nLength/sf
# close the file
file.close()

# cut the middle part of the audio data
timeOffset = 0
totalTime = np.int32(np.ceil(audioDataRawTotalTime - timeOffset -2))
totalPoint = totalTime*sf
timeOffsetPoint = timeOffset*sf
audioData = audioDataRaw[range(timeOffsetPoint,timeOffsetPoint+totalPoint)]

# set frequency
freq = 18000
# calculate time t
t = np.arange(totalPoint)/sf
# get cos and -sin used in demodulation
signalCos = np.cos(2*np.pi*freq*t)
signalSin = np.sin(2*np.pi*freq*t)
# get a butterworth filter
b, a = signal.butter(3, 50/(sf/2), 'lowpass')
# multiply received signal (audioData) and demodulation signal, also apply the filter
signalI = signal.filtfilt(b,a,audioData*signalCos)
signalQ = signal.filtfilt(b,a,audioData*signalSin)
# remove static vector
signalI = signalI - np.mean(signalI)
signalQ = signalQ - np.mean(signalQ)
# calculate the phase angle
phase = np.arctan(signalQ/signalI)
# unwrap the phase angle
phase = np.unwrap(phase*2)/2
# calculate the wave length
waveLength = 342/freq
# calculate distance
distance = phase/2/np.pi*waveLength/2

# plot the result
plt.figure(1)
# plt.plot(audioData)
# plt.plot(t,signalI)
# plt.plot(t,signalQ)
# plt.plot(signalI,signalQ)
# plt.plot(t,phase)
plt.plot(t,distance)
plt.xlabel("t/s")
plt.ylabel("distance/m")
plt.show()