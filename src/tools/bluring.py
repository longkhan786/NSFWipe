from langchain.tools import tool
from src.utils.utils import blur, to_ranges, analyze
import cv2


@tool("video_bluring")
def blur_video(video_path: str, output_path: str) -> str:
    """
    Blur video frames where nudity is detected
    """

    cap = cv2.VideoCapture(video_path)
    flagged_times = []

    if not cap.isOpened():
        raise RuntimeError("Cannot open video")

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_index = 0

    sample_rate = max(1, int(fps / 4))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        if frame_index % sample_rate == 0:
            timestamp = frame_index / fps
            if analyze(frame):
                flagged_times.append(timestamp)

        frame_index += 1

    cap.release()

    blur_ranges = to_ranges(flagged_times)
    
    output_path = f"{output_path}/blurred_output.mp4"
    blur(video_path, output_path, blur_ranges)

    return str(output_path)
