# tools/news_summary_tool.py
"""
News Summary Tool
-----------------
Uses OpenAI to summarize Tavily search results
into clean, short, factual bullet points.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_news(evidence_list: list) -> str:
    """
    Take raw Tavily search results and produce a concise summary.

    Args:
        evidence_list: list of dicts from Tavily

    Returns:
        summary: short text summary
    """

    if not evidence_list:
        return "No relevant news found."

    combined_text = "\n".join([item.get("content", "") for item in evidence_list])

    # Summarize using OpenAI
    prompt = f"""
    Summarize the following information into 3–5 concise bullet points.
    Focus on facts only. Avoid opinions.

    TEXT:
    {combined_text}
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=300,
            temperature=0.1,
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        print("[NEWS SUMMARY ERROR]:", e)
        return "Summary unavailable."
