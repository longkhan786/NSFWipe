import srt
import subprocess
import os
from datetime import timedelta
from faster_whisper import WhisperModel
from transcripts import translate_srt

_model = None

def load_model():
    global _model
    if _model is None:
        _model = WhisperModel("tiny", device="cpu", compute_type="int8")
    return _model

def extract_audio(video_path, output_audio="temp_audio.wav"):
    command = ["ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", output_audio]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(output_audio):
        raise RuntimeError("Audio extraction failed")

    return output_audio

def create_and_update_srt(srt_content):
    with open("generated-files/output_new.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)

def generate_subtitles(file, translate=False):
    audio_file = extract_audio(file)

    segments, info = load_model().transcribe(audio_file)
    segments = list(segments)

    print("Language:", info.language)

    subtitles = []
    for i, segment in enumerate(segments, start=1):
        subtitles.append(
            srt.Subtitle(
                index=i,
                start=timedelta(seconds=segment.start),
                end=timedelta(seconds=segment.end),
                content=segment.text.strip()
            )
        )

    create_and_update_srt(srt.compose(subtitles))

    if (translate): 
        translate_srt("generated-files/output_new.srt")

