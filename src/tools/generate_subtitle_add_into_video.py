from langchain.tools import tool
from src.utils.utils import extract_audio, create_and_update_srt
from src.models.subtitle import whisper
import srt
from datetime import timedelta
import cv2
import os

@tool("subtitle_generate_create_output_new_srt_file")
def subtitle_generate(video_path: str, output_path: str) -> str:
    """
    create audio file from video and generate subtitles
    """
    audio_file = extract_audio(video_path)

    segments, info = whisper.transcribe(audio_file)
    segments = list(segments)

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

    create_and_update_srt(srt.compose(subtitles), output_path)
    os.remove("temp_audio.wav")