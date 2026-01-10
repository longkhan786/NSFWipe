import cv2
from src.models import nsfw_classifier
from PIL import Image

flagged_times = []

def analyze(frame, timestamp):

    frame = cv2.resize(frame, (384, 384))

    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    image = Image.fromarray(frame)

    results = nsfw_classifier(image)

    for r in results:
        label = r["label"].lower()
        score = r["score"]
        print(f"Timestamp: {timestamp:.2f}s - {label}: {score:.4f}")

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
    out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))

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
