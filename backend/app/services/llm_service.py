import os
from groq import Groq

# Reuse the prompt logic from original project
IMPACT_PROMPT = """
You are a financial analyst. Analyze the following news for the stock: {ticker}.
News Title: {title}
News Summary: {summary}

1. Summarize the news in 1 short sentence.
2. Determine the impact on the stock price (Positive, Negative, Neutral).
3. Assign an "Impact Score" from 1 to 5 (5 being massive market-moving news).

Output format EXACTLY like this:
Summary: [Your summary here]
Impact: [Score] [Sentiment] (e.g. 5 Positive)
"""

def evaluate_news(ticker: str, title: str, summary: str) -> dict:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY not found.")
        return {"summary": "LLM Error", "impact": "0 Neutral"}

    client = Groq(api_key=api_key)

    try:
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": IMPACT_PROMPT.format(ticker=ticker, title=title, summary=summary)
                }
            ],
            model="llama-3.1-8b-instant",  # Updated from decommissioned llama3-8b-8192
        )
        
        response_text = completion.choices[0].message.content
        return parse_llm_response(response_text)

    except Exception as e:
        print(f"LLM Error: {e}")
        return {"summary": "LLM Failed", "impact": "0 Neutral"}

def parse_llm_response(response: str) -> dict:
    """
    Parses the structured output from the LLM.
    """
    summary = "No summary"
    impact = "0 Neutral"
    
    for line in response.splitlines():
        line = line.strip()
        if line.startswith("Summary:"):
            summary = line.replace("Summary:", "").strip()
        elif line.startswith("Impact:"):
            impact = line.replace("Impact:", "").strip()
            
    return {"summary": summary, "impact": impact}
