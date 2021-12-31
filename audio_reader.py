import pyaudio
import wave
from re import match



p = pyaudio.PyAudio()
print(p.get_device_count())
cable_input_devices = []
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    if match(r'CABLE Input.*\)', info["name"]):
        cable_input_devices.append(info["index"])


for info in [p.get_device_info_by_index(i) for i in cable_input_devices]:
    print(info)

cable_index = cable_input_devices[-1]
cable_info = p.get_device_info_by_index(cable_index)

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = cable_info["maxOutputChannels"]
RATE = cable_info["defaultSampleRate"]

stream = p.open(format = FORMAT,
   channels = CHANNELS,
   rate = RATE,
   input = True,
   frames_per_buffer = CHUNK)

