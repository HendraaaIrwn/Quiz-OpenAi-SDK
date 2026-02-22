import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()


def get_client() -> OpenAI:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found. Set OPENAI_API_KEY in your .env file.")

    return OpenAI(api_key=api_key)
