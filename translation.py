import os
import whisper

model = whisper.load_model("turbo")
result = model.transcribe(os.path.join(__file__, "final_combined_audio.wav"),fp16=False) 

with open("./translate.txt", "w") as f:
    text = str(result.get('text') )
    print(text)
    f.write(text)
