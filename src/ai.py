import whisper

def translate_audio(path_to_sound_file):
    print("\nTranscribing audio...")
    model = whisper.load_model("turbo")
    result = model.transcribe(path_to_sound_file,fp16=False, language="ru")
    print("Transcription complete.")
    with open("./translate.txt", "w") as f:
        text = str(result.get('text') )
        print(text)
        f.write(text)

