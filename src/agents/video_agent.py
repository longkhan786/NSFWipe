from langchain_core.messages import HumanMessage
from src.models import agent

def run_full_pipeline(video_path: str, output_path: str):
    response = agent.invoke({
        "messages": [
            HumanMessage(
                content=f"""
                Step 1: generate subtitles and burn them into video.
                input_video: {video_path}
                output_dir: {output_path}

                Step 2: detect nudity and blur if needed.
                """
            )
        ]
    })

    return response
