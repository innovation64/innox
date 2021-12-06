# readme

由于树莓派性能限制，可能无法实现在树莓派上进行实时数据处理
可以将音频数据通过网络实时传输至个人电脑进行处理,这里提供一个demo

此文件夹包含以下文件：
```
树莓派：
    query_device.py 列出树莓派上所有的音频设备接口，后面编程时需要
    play.py 用于播放音频文件
    18000L.wav 音频文件，采样频率48kHz，左声道声波频率18kHz，右声道静音
    client.py 用于实时录音并将数据发送至个人电脑，并保存至record.wav
    phase.py  离线处理音频数据示例
个人电脑：
    demo.m  展示实时距离变化的MATLAB脚本
```

依赖软件包：

pyaudio：https://people.csail.mit.edu/hubert/pyaudio/

scipy：https://scipy.org/



运行说明：

0 在树莓派上安装所需的依赖；运行query_device.py，列出树莓派上所有的音频设备接口，修改play.py中的utput_device_index和client.py中的input_device_index；修改client.py中的IP为个人电脑的IP。

1 在个人电脑中使用MATLAB打开 demo.m，点击运行。

2 在树莓派终端中依次运行 play.py 和 client.py。