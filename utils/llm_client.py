from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL, TEMPERATURE, MAX_TOKENS

client = OpenAI(api_key=OPENAI_API_KEY)

def call_llm(prompt: str) -> str:
    response = client.chat.completions.create(
        model=LLM_MODEL,
        temperature=TEMPERATURE,
        max_tokens=MAX_TOKENS,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()
