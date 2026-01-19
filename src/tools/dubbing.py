from langchain.tools import tool
from src.utils.utils import extract_audio, create_srt_file_using_audio
from src.models.elevenLabs import elevenLabsAgent
import os
import subprocess
from TTS.api import TTS


device = "cpu"
tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(device)

os.makedirs("tts", exist_ok=True)

def save_video(input_video, output_path):

    cmd = [
        "ffmpeg", "-y",
        "-i", input_video,
        "-i", "output.wav",
        "-map", "0:v",
        "-map", "1:a",
        "-c:v", "copy",
        "-shortest",
        f"{output_path}/dubb_output.mp4"
    ]
    subprocess.run(cmd)

@tool("dubb_video_create_dubbed_video")
def dubb_video(video_path: str, output_path: str) -> str:
    """
    Dub video in a different language
     args:
        video_path: it means full path of video with video name
        output_path: it means when video is generated where video will store

    return:
        it will return the full path of video with video name
    """

    audio_file = extract_audio(video_path, output_audio="temp_audio.wav")
    spoken_texts_in_video = create_srt_file_using_audio(audio_file, output_path, True)
    print("Translated Texts: ", spoken_texts_in_video)
    
    tts.tts_to_file(
        text=spoken_texts_in_video,
        speaker_wav="audio.wav",
        language="en",
        file_path="output.wav"
    )

    save_video(video_path, output_path)

    return os.path.abspath(f"{output_path}/dubb_output.mp4")
