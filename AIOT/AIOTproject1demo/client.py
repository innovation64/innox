import pyaudio
import wave
import time
import socket

# socket
SERVER_HOST = '10.16.26.128' #PC的IP地址，可通过cmd>ipconfig命令查看
SERVER_PORT = 12345 #端口，自定义
s = socket.socket()
s.connect((SERVER_HOST, SERVER_PORT))


# record parameters
CHUNK = 4800
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 48000    #采样率
RECORD_SECONDS = 300
WAVE_OUTPUT_FILENAME = "record.wav"

p = pyaudio.PyAudio()

# record file info
recordFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
recordFile.setnchannels(CHANNELS)
recordFile.setsampwidth(p.get_sample_size(FORMAT))
recordFile.setframerate(RATE)

# record callback
def recordCallback(in_data, frame_count, time_info, status):
    #print(len(in_data))
    recordFile.writeframes(in_data)
    s.send(in_data)
    return (in_data, pyaudio.paContinue)

# open record stream
recordStream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                input_device_index=10,  #此处需要设置为ac108的index
                frames_per_buffer=CHUNK,
                stream_callback=recordCallback)

print("recording")

t = 0
while t<RECORD_SECONDS:
    time.sleep(1)
    t = t + 1
    print(t)
    
print("done recording")

# stop record stream
recordStream.stop_stream()
recordStream.close()
recordFile.close()

# close PyAudio
p.terminate()

# close socket
s.close()
