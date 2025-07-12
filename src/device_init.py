import subprocess
import os
from dotenv import load_dotenv
import soundcard 

def print_available_devices():
    result = subprocess.run(["SwitchAudioSource", "-a"], capture_output=True, text=True)
    print("Available capture devices:")
    print(result.stdout)

def init_blackhole():
    load_dotenv(verbose=True, dotenv_path='./.env', override=True)
    capture_device_name = os.getenv("capture_device_name")

    if not capture_device_name:
        print("capture_device_name is not set. Please set it in your .env file.") 
        print_available_devices()
        exit(1)
    
    result = subprocess.run(["SwitchAudioSource", "-s", capture_device_name])
    if result.returncode == 1:
        print("Failed to switch output sound device. Please ensure the device name is correct.")
        print_available_devices()
        exit(1)

def select_microphone():
    microphones = soundcard.all_microphones()
    for i, mic in enumerate(microphones):
        print(f"{i}: {mic.name}")
    mic_index = int(input("Select microphone index: "))
    if mic_index < 0 or mic_index >= len(microphones):
        print("Invalid microphone index selected.")
        exit(1)
    selected_mic = microphones[mic_index]
    name = selected_mic.name
    print(f"Selected microphone: {name}")
    return name
        

