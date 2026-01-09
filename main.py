import cv2
from utils import analyze

video_path = "assets/converted.mp4"
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
