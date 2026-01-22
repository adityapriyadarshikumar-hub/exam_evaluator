from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL, TEMPERATURE, MAX_TOKENS
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

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
    time.sleep(2)  # Delay to avoid rate limits
    return response.choices[0].message.content.strip()

def compute_similarity(text1: str, text2: str) -> float:
    # Get embeddings
    emb1 = client.embeddings.create(input=text1, model="text-embedding-3-small").data[0].embedding
    emb2 = client.embeddings.create(input=text2, model="text-embedding-3-small").data[0].embedding
    # Compute cosine similarity
    similarity = cosine_similarity([emb1], [emb2])[0][0]
    return similarity
