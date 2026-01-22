from openai import OpenAI
from config import OPENAI_API_KEY, LLM_MODEL, TEMPERATURE, MAX_TOKENS
import time
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
from transformers import pipeline
import torch

client = OpenAI(api_key=OPENAI_API_KEY)

# Local models
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')  # Local embeddings
llm_pipeline = pipeline("text2text-generation", model="google/flan-t5-small", device=0 if torch.cuda.is_available() else -1)  # Local LLM

def call_llm(prompt: str, force_openai: bool = False) -> str:
    if force_openai:
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
    # Try local LLM first
    try:
        # flan-t5 may not support temperature, so use default
        result = llm_pipeline(prompt, max_new_tokens=MAX_TOKENS)
        return result[0]['generated_text'].strip()
    except Exception as e:
        print(f"Local LLM failed: {e}, falling back to OpenAI")
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
    # Use local embeddings
    try:
        emb1 = embedding_model.encode(text1)
        emb2 = embedding_model.encode(text2)
        similarity = cosine_similarity([emb1], [emb2])[0][0]
        return float(similarity)
    except Exception as e:
        print(f"Local embedding failed: {e}, falling back to OpenAI")
        # Fallback to OpenAI embeddings
        emb1 = client.embeddings.create(input=text1, model="text-embedding-3-small").data[0].embedding
        emb2 = client.embeddings.create(input=text2, model="text-embedding-3-small").data[0].embedding
        similarity = cosine_similarity([emb1], [emb2])[0][0]
        return float(similarity)
