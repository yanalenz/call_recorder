import os
import whisper

def translate_audio(path_to_sound_file):
    print("translating audio")
    model = whisper.load_model("turbo")
    result = model.transcribe(path_to_sound_file,fp16=False) 

    with open("./translate.txt", "w") as f:
        text = str(result.get('text') )
        print(text)
        f.write(text)
    print("audio translated")

