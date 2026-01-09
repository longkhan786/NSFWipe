import cv2
from transformers import pipeline
from PIL import Image

nsfw_classifier = pipeline(
    "image-classification",
    model="Falconsai/nsfw_image_detection",
    device=-1  # CPU
)

def cv2_to_pil(frame):
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    return Image.fromarray(frame)

flagged_times = []

def analyze(frame, timestamp):
    frame = cv2.resize(frame, (384, 384))

    image = cv2_to_pil(frame)


    results = nsfw_classifier(image)

    for r in results:
        label = r["label"].lower()
        score = r["score"]

        if label == "nsfw" and score >= 0.6:
            filename = f"generated-files/frame_{timestamp:.2f}.jpg"
            image.save(filename)
            flagged_times.append(timestamp)
            break


video_path = "assets/Toxic_Introducing_Raya_Rocking_Star_Yash_Geetu_Mohandas_KVN_Productions_Monster_Mind_Creations_1080P.mp4"
cap = cv2.VideoCapture(video_path)

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
        analyze(frame, timestamp)

    frame_index += 1

cap.release()

print("\n✅ FINAL FLAGGED TIMESTAMPS")
print(flagged_times)
