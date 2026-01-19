from langchain.tools import tool
from src.utils.utils import extract_audio, create_srt_file_using_audio
from src.models.subtitle import whisper
import srt
from datetime import timedelta
import os
from moviepy import VideoFileClip, TextClip, CompositeVideoClip
import pysrt

@tool("subtitle_generate_create_output_new_srt_file")
def subtitle_generate(video_path: str, output_path: str) -> str:
    """
    create audio file from video and generate subtitles and add to the video

    args:
        video_path: it means full path of video with video name
        output_path: It means directory folder where videos will store

    return:
        it will return the full path of video with video name
    """

    print(f"subtitle_generate_create_output_new_srt_file \n video path:{video_path} \n output_path: {output_path}")
    audio_file = extract_audio(video_path)

    subititle_srt_file_path = create_srt_file_using_audio(audio_file, output_path)

    selected_video = VideoFileClip(video_path)
    
    subtitles = pysrt.open(subititle_srt_file_path)
    subtitle_clips = []

    for sub in subtitles:
        start = sub.start.ordinal / 1000
        end = sub.end.ordinal / 1000
        duration = end - start

        txt_clip = (
            TextClip(
                text=sub.text.replace("\n", " "),
                font_size=25,
                color="white",
                stroke_color="black",
                stroke_width=2,
                method="caption",
                size=(int(selected_video.w * 0.7), None),
                text_align="center"
            )
            .with_start(start)
            .with_duration(duration)
            .with_position(("center", selected_video.h - 250))
        )

        subtitle_clips.append(txt_clip)
    
    final_video = CompositeVideoClip(
        [selected_video] + subtitle_clips,
        size=selected_video.size
    )

    final_video.write_videofile(
        f"{output_path}/output_with_subtitles.mp4",
        fps=selected_video.fps,
        codec="libx264",
        audio_codec="aac",
        preset="medium",
        threads=4
    )

    return f"{output_path}/output_with_subtitles.mp4"







