import os
import whisper

def translate_audio(pathToSoundFile):
    print("translating audio")
    model = whisper.load_model("turbo")
    result = model.transcribe(pathToSoundFile,fp16=False) 

    with open("./translate.txt", "w") as f:
        text = str(result.get('text') )
        print(text)
        f.write(text)
    print("audio translated")

