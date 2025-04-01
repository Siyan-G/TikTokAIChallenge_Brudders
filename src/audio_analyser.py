import whisper


def transcribe_audio(audio_file):
    """
    Transcribe audio file using Whisper model.
    """
    # Load the Whisper model
    # Note: You can choose different models like "tiny", "base", "small", "medium", "large"
    model = whisper.load_model("base")
    result = model.transcribe(audio_file, language="en")
    print(result["text"])

transcribe_audio("data/audio/car_crash.m4a")
transcribe_audio("data/audio/ina2.m4a")