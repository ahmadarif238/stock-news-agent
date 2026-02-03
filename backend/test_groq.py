import os
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
print(f"Testing API Key: {api_key[:10]}...")

try:
    client = Groq(api_key=api_key)
    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": "test"}],
        model="llama-3.1-8b-instant",
    )
    print("Success!")
    print(f"Response: {completion.choices[0].message.content}")
except Exception as e:
    print(f"Errors: {e}")
