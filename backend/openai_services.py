import os
import openai
from dotenv import load_dotenv

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


if __name__ == "__main__":
    test_prompt = "What are some tips for answering behavioral interview questions?"
    print("Test prompt:", test_prompt)
    print("GPT response:", get_gpt_response(test_prompt))
