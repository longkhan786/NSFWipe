import cv2
from src.utils import analyze
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
video_path = BASE_DIR / "assets" / "Toxic_Introducing_Raya_Rocking_Star_Yash_Geetu_Mohandas_KVN_Productions_Monster_Mind_Creations_360P.mp4"
cap = cv2.VideoCapture(video_path)
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
        is_nsfw = analyze(frame)

        if is_nsfw:
            flagged_times.append(timestamp)

    frame_index += 1

cap.release()

print("\n✅ FINAL FLAGGED TIMESTAMPS")
print(flagged_times)
