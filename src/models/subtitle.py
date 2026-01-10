from faster_whisper import WhisperModel

whisper = WhisperModel(
    "tiny", 
    device="cpu", 
    compute_type="int8"
)