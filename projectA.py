# переключить на "поток захвата"
import pyaudio
import wave
import os

audio = pyaudio.PyAudio() 

info = audio.get_host_api_info_by_index(0) 
numdevices = info.get('deviceCount')  # переменная, в которой сохраняется количество устройств

# declare emty var 
blackhole_device_index = -1 # ищет тут нужные нам устройства ,тк пока не нашли их , значение -1
microphone_device_index = -1 

if type(numdevices) is int: # дополнительная проверка на то, что устройства есть
    for i in range(0, numdevices): # проверка с нуля до кол-ва найденных устройств 
        deviceInfo = audio.get_device_info_by_host_api_device_index(0, i) # (0) - индекс Host API, i = индекс конкретного устр-ва
        name = deviceInfo['name'] 
        if name == 'BlackHole 2ch':
            blackhole_device_index = i
        if name == 'Микрофон MacBook Pro':
            microphone_device_index = i

if blackhole_device_index == -1:
    print("No input device found")
    exit() 

if microphone_device_index == -1:
    print("No input device found")
    exit()

system_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2048, input_device_index=blackhole_device_index)
microphone_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2048, input_device_index=microphone_device_index)

frames = []
frames2 = []

try:
    while True:
        data = system_stream.read(2048, exception_on_overflow=True) # 2048 фреймов (read) 
        frames.append(data)

        data2 = microphone_stream.read(2048, exception_on_overflow=True) 
        frames2.append(data2)
except KeyboardInterrupt:
    print("Stopping")
    pass

filepath = os.path.join(os.path.dirname(__file__), 'system.wav')
sound_file = wave.open(filepath, 'wb')
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(48000)
sound_file.writeframes(b''.join(frames))
sound_file.close()

filepath = os.path.join(os.path.dirname(__file__), 'microphone.wav')
sound_file2 = wave.open(filepath, 'wb')
sound_file2.setnchannels(1)
sound_file2.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file2.setframerate(48000)
sound_file2.writeframes(b''.join(frames2))
sound_file2.close()

system_stream.stop_stream()
system_stream.close()
microphone_stream.stop_stream()
microphone_stream.close()
audio.terminate()
