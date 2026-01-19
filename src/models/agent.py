from langchain.agents import create_agent
from src.tools.bluring import blur_video
from src.tools.generate_subtitle_add_into_video import subtitle_generate
from src.tools.dubbing import dubb_video
from langchain.chat_models import init_chat_model

llm = init_chat_model(
    model="qwen/qwen3-32b",
    model_provider="groq"
)

agent = create_agent(
    model=llm,
    tools=[blur_video, subtitle_generate, dubb_video],
)
