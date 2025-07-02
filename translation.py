import whisper

model = whisper.load_model("turbo")
result = model.transcribe("/Users/murmur/Documents/python/project1/myrecording.wav",fp16=False) 

with open("./translate.txt", "w") as f:
    text = str(result.get('text') )
    print(text)
    f.write(text)
