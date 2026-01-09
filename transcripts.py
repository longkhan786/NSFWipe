import os
from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
import srt

load_dotenv()
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# Initialize Groq LLM
model = init_chat_model("groq:qwen/qwen3-32b")


def translate_srt(input_file: str, output_file: str = "output_hi.srt", target_language: str = "Hindi"):
    """
    Translate an SRT file to a target language using Groq LLM.
    Ensures output contains only the translated text, no reasoning.
    """
    # Read SRT file
    with open(input_file, "r", encoding="utf-8") as f:
        srt_content = f.read()

    subtitles = list(srt.parse(srt_content))

    for sub in subtitles:
        # Strong prompt to avoid reasoning
        prompt = f"""
            Translate ONLY the following text into {target_language}.
            Do NOT include any explanations, reasoning, or extra text.
            Output ONLY the translated text.

            Text:
            {sub.content}
        """
        response = model.invoke(prompt)
        sub.content = response.content.strip()

    translated_srt = srt.compose(subtitles)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(translated_srt)

    print(f"✅ Translated SRT saved as: {output_file}")
