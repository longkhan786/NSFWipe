import cv2
from PIL import Image
from src.models.nsfw import nsfw_classifier
from src.models.subtitle import whisper
import subprocess
import os
import srt
from datetime import timedelta
from transformers import MarianMTModel, MarianTokenizer


def analyze(frame):
    frame = cv2.resize(frame, (384, 384))
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    results = nsfw_classifier(image)

    for r in results:
        label = r["label"].lower()
        score = r["score"]

        if label == "nsfw" and score >= 0.6:
            return True

    return False

def to_ranges(timestamps, padding=0.5):
    return [(max(0, t - padding), t + padding) for t in timestamps]

def blur(input_path, output_path, blur_ranges):

    cap = cv2.VideoCapture(input_path)
    fps = cap.get(cv2.CAP_PROP_FPS)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    out = cv2.VideoWriter(str(output_path), fourcc, fps, (width, height))

    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        timestamp = frame_index / fps

        for start, end in blur_ranges:
            if start <= timestamp <= end:
                frame = cv2.GaussianBlur(frame, (51, 51), 0)
                break

        out.write(frame)
        frame_index += 1

    cap.release()
    out.release()

def extract_audio(video_path, output_audio="temp_audio.wav"):

    command = ["ffmpeg", "-y", "-i", video_path, "-ac", "1", "-ar", "16000", output_audio]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    if not os.path.exists(output_audio):
        raise RuntimeError("Audio extraction failed")

    return output_audio

def create_and_update_srt(srt_content, output_path):
    with open(f"{output_path}/output_new.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)

    return f"{output_path}/output_new.srt"

def create_srt_file_using_audio(audio_file, output_path, only_text=False):
    segments, info = whisper.transcribe(audio_file)
    segments = list(segments)

    subtitles = []
    texts = ''
    for i, segment in enumerate(segments, start=1):
        if only_text:
            texts += segment.text.strip() + " "
        else:
            subtitles.append(
                srt.Subtitle(
                    index=i,
                    start=timedelta(seconds=segment.start),
                    end=timedelta(seconds=segment.end),
                    content=segment.text.strip()
                )
            )
            subititle_srt_file_path = create_and_update_srt(srt.compose(subtitles), output_path)

    return texts if only_text else subititle_srt_file_path

    
model_name = "Helsinki-NLP/opus-mt-en-hi"
tokenizer = MarianTokenizer.from_pretrained(model_name)
model = MarianMTModel.from_pretrained(model_name)

def translate_to_hindi(text):
    tokens = tokenizer(text, return_tensors="pt", padding=True)
    translated = model.generate(**tokens)
    return tokenizer.decode(translated[0], skip_special_tokens=True)