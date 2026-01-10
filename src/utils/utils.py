import cv2
from PIL import Image
from src.models.nsfw import nsfw_classifier
import subprocess
import os

def analyze(frame, timestamp):
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

    fourcc = cv2.VideoWriter_fourcc(*"XVID")
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

def create_and_update_srt(srt_content):
    with open("output_new.srt", "w", encoding="utf-8") as f:
        f.write(srt_content)

    

