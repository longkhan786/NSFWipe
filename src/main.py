import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


from pathlib import Path
from langchain_core.messages import HumanMessage
from src.models import agent


BASE_DIR = Path(__file__).resolve().parent
input_video = BASE_DIR / "assets" / "Toxic_Introducing_Raya_Rocking_Star_Yash_Geetu_Mohandas_KVN_Productions_Monster_Mind_Creations_360P.mp4"

response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=
                f"""
                    Could you please create a audio file and generate subtitles ? video path: {input_video}.
                    Could you please blur this video {input_video} where nudity find ? 
                """
            )
        ]
    }
)

print(f"Messages : {response['messages']}")
