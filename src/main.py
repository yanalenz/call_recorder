# switch to "capture stream"
import audio_joiner 
import ai
import pyaudio
import wave
import os
import datetime as dt 


from device_init import init_blackhole, select_microphone

init_blackhole()
audio = pyaudio.PyAudio() 

info = audio.get_host_api_info_by_index(0) 
numdevices = info.get('deviceCount')  # variable, where the number of devices is saved

# declare emty var 
blackhole_device_index = -1 # looking here for the needed devices, because we haven't found them yet, the value -1
microphone_device_index = -1 
microphone_device_name = select_microphone()

if type(numdevices) is int: # checking additionally that devices exist
    for i in range(0, numdevices): # checking found devices
        deviceInfo = audio.get_device_info_by_host_api_device_index(0, i) # (0) - indecs Host API, i = indecs of the specific device
        name = deviceInfo['name'] 
        if name == 'BlackHole 2ch':
            blackhole_device_index = i
        if name == microphone_device_name:
            microphone_device_index = i

if blackhole_device_index == -1:
    print("No blackhole device found")
    exit() 

if microphone_device_index == -1:
    print("No microphone device found")
    exit()

system_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2048, input_device_index=blackhole_device_index)
microphone_stream = audio.open(format=pyaudio.paInt16, channels=1, rate=48000, input=True, frames_per_buffer=2048, input_device_index=microphone_device_index)

frames = []
frames2 = []

try:
    while True:
        data = system_stream.read(2048, exception_on_overflow=True) # 2048 frames (read) 
        frames.append(data)

        data2 = microphone_stream.read(2048, exception_on_overflow=True) 
        frames2.append(data2)
except KeyboardInterrupt:
    pass 

wav_1 = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
systemSoundFilePath = os.path.join(os.path.dirname(__file__), f'../temp/system_{wav_1}.wav')
sound_file = wave.open(systemSoundFilePath, 'wb')
sound_file.setnchannels(1)
sound_file.setsampwidth(audio.get_sample_size(pyaudio.paInt16))
sound_file.setframerate(48000)
sound_file.writeframes(b''.join(frames))
sound_file.close()

wav_2 = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
voiceFilePath = os.path.join(os.path.dirname(__file__), f'../temp/microphone_{wav_2}.wav')
sound_file2 = wave.open(voiceFilePath, 'wb')
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

final_wav = dt.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
joined_audio_file_path = os.path.join(os.path.dirname(__file__), f"{final_wav}.wav")
audio_joiner.join_audio(systemSoundFilePath, voiceFilePath, joined_audio_file_path)
ai.translate_audio(joined_audio_file_path)