
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ[""])

def query_llm(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )OPENAI_API_KEY

    return response.output_text