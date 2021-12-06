# 列出音频设备信息
import pyaudio

p=pyaudio.PyAudio()
for i in range(p.get_device_count()):
    print(p.get_device_info_by_index(i))


# 如果使用sounddevice
# import sounddevice as sd
# sd.query_devices()