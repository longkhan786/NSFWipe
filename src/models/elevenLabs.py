from elevenlabs.client import ElevenLabs
import os

elevenLabsAgent = ElevenLabs(
    api_key=os.getenv("ELEVENLABS_API_KEY")
)