from groq import Groq
from config import GROQ_API_KEY

client = Groq(api_key=GROQ_API_KEY)

def evaluate_news_with_llm(news_item, prompt_template):
    try:
        content = f"{prompt_template}\n\nTitle: {news_item['title']}\n\nSummary: {news_item['summary']}"

        response = client.chat.completions.create(
            model="llama3-8b-8192",  # Changed model
            messages=[{"role": "user", "content": content}],
            temperature=0.7,
            top_p=0.95,
            max_tokens=1024,  # Groq-compatible param (not max_completion_tokens)
            stream=True,
            stop=None
        )

        full_response = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                full_response += chunk.choices[0].delta.content
        return full_response

    except Exception as e:
        print(f"Error from Groq API: {e}")
        return "Summary: Could not evaluate\nImpact Score: 🔈"
