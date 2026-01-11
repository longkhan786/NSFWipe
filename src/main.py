import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

from pathlib import Path
from langchain_core.messages import HumanMessage
from src.models import agent


BASE_DIR = Path(__file__).resolve().parent
input_video = BASE_DIR / "assets" / "Toxic_Introducing_Raya_Rocking_Star_Yash_Geetu_Mohandas_KVN_Productions_Monster_Mind_Creations_360P.mp4"
output_path = BASE_DIR / "assets" / "outputs"

response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=
                f"""
                    could you please generate the subtitle and add to the video ? 

                    input path: {input_video} 
                    you can save outputs here: {output_path}
                """
            )
        ]
    }
)

print(f"Messages : {response['messages']}")


response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=
                f"""
                    could you please find nudity, if it has then blur it ? 

                    video_path: {output_path}/output_with_subtitles.mp4 
                    you can save outputs here: {output_path}
                """
            )
        ]
    }
)
