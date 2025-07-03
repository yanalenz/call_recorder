
import os
# fddf
def join_audio(audio1, audio2):
    # we need to run ffmpeg and pass this path as an argument
    ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
    # run test command to check if ffmpeg is installed
    if not os.path.exists(ffmpeg_path):
        print("ffmpeg is not installed. Please install it and try again.")
        return

    # run ffmpeg command to join the two audio files
    os.system(f"{ffmpeg_path}")


join_audio("system.wav", "microphone.wav")