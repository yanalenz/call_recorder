import subprocess
import os
from dotenv import load_dotenv

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