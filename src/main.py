import os
from dotenv import load_dotenv

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")


from pathlib import Path
from langchain_core.messages import HumanMessage
from src.models import agent


BASE_DIR = Path(__file__).resolve().parent
input_video = BASE_DIR / "assets" / "m2-res_480p.mp4"
output_path = BASE_DIR / "assets" / "outputs"

response = agent.invoke(
    {
        "messages": [
            HumanMessage(
                content=
                f"""
                    Could you please blur this video {input_video} where nudity find ? 

                    you can save outputs here: {output_path}
                """
            )
        ]
    }
)

print(f"Messages : {response['messages']}")
