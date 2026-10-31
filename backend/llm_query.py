
import os
from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=os.environ["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"])

def query_llm(prompt: str) -> str:
    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )OPENAI_API_KEY

    return response.output_text