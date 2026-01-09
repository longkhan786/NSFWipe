import cv2
from src.utils import analyze, blur_video
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
input_video = BASE_DIR / "assets" / "Toxic_Introducing_Raya_Rocking_Star_Yash_Geetu_Mohandas_KVN_Productions_Monster_Mind_Creations_360P.mp4"
output_video = BASE_DIR / "assets" / "blurred_output.mp4"

cap = cv2.VideoCapture(input_video)
flagged_times = []

if not cap.isOpened():
    raise RuntimeError("❌ Cannot open video")

fps = cap.get(cv2.CAP_PROP_FPS)
frame_index = 0

sample_rate = max(1, int(fps / 4))

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if frame_index % sample_rate == 0:
        timestamp = frame_index / fps
        if analyze(frame, timestamp):
            flagged_times.append(timestamp)

    frame_index += 1

cap.release()

def to_ranges(timestamps, padding=0.5):
    return [(max(0, t - padding), t + padding) for t in timestamps]


blur_ranges = to_ranges(flagged_times)

print("Blur rangs:", blur_ranges)

blur_video(
    str(input_video),
    str(output_video),
    blur_ranges
)

print("Blurred video:", output_video)
