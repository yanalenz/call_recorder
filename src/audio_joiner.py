import os
import subprocess

def join_audio(audio1, audio2, output_file_path = "combined_audio.wav"):
    # we need to run ffmpeg and pass this path as an argument
    ffmpeg_path = "/opt/homebrew/bin/ffmpeg"
    # run test command to check if ffmpeg is installed
    if not os.path.exists(ffmpeg_path):
        print("ffmpeg is not installed. Please install it and try again.")
        return

    # using a filter complex to join the audio streams, [0:a] and [1:a] this is a inputs,
    #  a - audio stream from the first and second input files respectively.
    #  out - this is the name of the output stream, which will then be displayed with the -map [out] option.
    # -y - overwrite the output file if it already exists.
    command = [
        ffmpeg_path,
        '-i', audio1,
        '-i', audio2,
        '-filter_complex', '[0:a][1:a]amix=inputs=2[out]',
        '-map', '[out]',
        '-y', 
        output_file_path
    ]

    try:
        subprocess.run(command, capture_output=True, text=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error during FFmpeg execution:")
        print(f"Command: {e.cmd}")
        print(f"Return code: {e.returncode}")
        print(f"Stdout: {e.stdout}")
        print(f"Stderr: {e.stderr}")
    except FileNotFoundError:
        print(f"Error: FFmpeg not found. Make sure that '{ffmpeg_path}' is the correct path.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


