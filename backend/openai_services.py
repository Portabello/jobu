import os
import openai
from dotenv import load_dotenv
import numpy as np

# Load environment variables from .env file
load_dotenv()

# Set your OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

SYSTEM_PROMPT = "You are a helpful assistant."

def get_gpt_response(user_message: str, model: str = "gpt-3.5-turbo") -> str:
    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_message},
            ],
            temperature=0.7,
            max_tokens=300,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

#RAG
# Global in-memory vector store
embedded_resume_chunks = []

def embed_texts(texts):
    response = openai.embeddings.create(
        model="text-embedding-3-small",
        input=texts
    )
    return [np.array(d.embedding) for d in response.data]

def add_resume_to_store(chunks, embeddings):
    global embedded_resume_chunks
    embedded_resume_chunks = list(zip(chunks, embeddings))

def get_resume_context(query: str, top_k: int = 3) -> str:
    if not embedded_resume_chunks:
        return ""

    query_embedding = embed_texts([query])[0]

    def cosine_sim(a, b):
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    sorted_chunks = sorted(
        embedded_resume_chunks,
        key=lambda x: cosine_sim(query_embedding, x[1]),
        reverse=True
    )

    top_chunks = [chunk for chunk, _ in sorted_chunks[:top_k]]
    return "\n\n".join(top_chunks)


if __name__ == "__main__":
    test_prompt = "What are some tips for answering behavioral interview questions?"
    print("Test prompt:", test_prompt)
    print("GPT response:", get_gpt_response(test_prompt))
