import pyaudio
import wave
import time
import numpy as np
from scipy import signal
from pixel_ring import main, pixel_ring
from gpiozero import LED

# record file info
power = LED(5)
power.on()
pixel_ring.set_brightness(50)

_VARS = {'distance': np.array([]),
         'distance0.1': np.array([]),
         'distance1': np.array([]),
         'myflag': False,
         'audioData': np.array([]),
         '0.1sData': np.array([])}

# record parameters
CHUNK = 4800
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000    #采样率
RECORD_SECONDS = float("inf")
# RECORD_SECONDS = 20
WAVE_OUTPUT_FILENAME = "./audio/output.wav"
p2= pyaudio.PyAudio()

filename = './audio/18000L.wav'
wf = wave.open(filename, 'rb')
# instantiate PyAudio (1)
p1 = pyaudio.PyAudio()


recordFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
recordFile.setnchannels(CHANNELS)
recordFile.setsampwidth(p2.get_sample_size(FORMAT))
recordFile.setframerate(RATE)

# define callback (2)
def callback(in_data, frame_count, time_info, status):
    data = wf.readframes(frame_count)
    return (data, pyaudio.paContinue)

# function
def recordCallback(in_data, frame_count, time_info, status):
    # global myflag
    recordFile.writeframes(in_data)
    _VARS['0.1sData'] = np.frombuffer(in_data,dtype='int16')
    _VARS['audioData'] = np.append(_VARS['audioData'] ,_VARS['0.1sData'] )
    return (in_data, pyaudio.paContinue)


def getdistance(audioData):
    freq = 18000
    fs = RATE
    c = 343
    t = np.arange(len(audioData))/fs
    signalCos = np.cos(2*np.pi*freq*t)
    signalSin = np.sin(2*np.pi*freq*t)
    b, a = signal.butter(3, 50/(fs/2), 'lowpass')
    signalI = signal.filtfilt(b,a,audioData*signalCos)
    signalQ = signal.filtfilt(b,a,audioData*signalSin)
    signalI = signalI - np.mean(signalI)
    signalQ = signalQ - np.mean(signalQ)
    phase = np.arctan(signalQ/signalI)
    phase = np.unwrap(phase*2)/2
    distance = c*phase/(4*np.pi*freq)
    return distance[-1]

# start the stream (4)
def start():
    WAVE_OUTPUT_FILENAME = "./audio/output.wav"
    p2= pyaudio.PyAudio()

    filename = './audio/18000L.wav'
    wf = wave.open(filename, 'rb')
    # instantiate PyAudio (1)
    p1 = pyaudio.PyAudio()


    recordFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
    recordFile.setnchannels(CHANNELS)
    recordFile.setsampwidth(p2.get_sample_size(FORMAT))
    recordFile.setframerate(RATE)
    # open stream using callback (3)
    stream = p1.open(format=p1.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    output_device_index=12,     #此处设置为ac101的index
                    stream_callback=callback)
    # open record stream
    recordStream = p2.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    input_device_index=10,  #此处需要设置为ac108的index
                    frames_per_buffer=CHUNK,
                    stream_callback=recordCallback)
    stream.start_stream()

    t = 0
    time.sleep(1)
    while t<RECORD_SECONDS:
        t+=1
        _VARS['distance1'] = getdistance(_VARS['audioData'])
        _VARS['distance'] = np.append(_VARS['distance']  ,_VARS['distance1'] )
        print (_VARS['distance1'])
    
        if _VARS['distance'][-1] >= 0.1 or _VARS['distance'][-1] <= -0.1 :
            print ('1')
            _VARS['myflag'] = True
            pixel_ring.think()

        elif _VARS['distance'][-1] < 0.1 and _VARS['distance'][-1] > -0.1 :
            print ('0')
            _VARS['myflag'] = False
            pixel_ring.off()

        else:
            print ('0')
            _VARS['myflag'] = False     
            pixel_ring.speak()
        
    print("done recording")

    # stop stream (6)
    stream.stop_stream()
    stream.close()
    wf.close()
    # stop record stream
    recordStream.stop_stream()
    recordStream.close()
    recordFile.close()

    # close PyAudio (7)
    p1.terminate()
    p2.terminate()

if __name__=="__main__":
    start()