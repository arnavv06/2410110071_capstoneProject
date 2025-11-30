# tools/search_tool.py
"""
Tavily Web Search Tool
----------------------
Provides structured web search results for Supporter and Critic.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
TAVILY_ENDPOINT = "https://api.tavily.com/search"


def search_tavily(query: str, max_results: int = 5) -> list:
    if not TAVILY_API_KEY:
        print("[WARNING] Missing TAVILY_API_KEY")
        return []

    payload = {
        "api_key": TAVILY_API_KEY,
        "query": query,
        "max_results": max_results
    }

    try:
        res = requests.post(TAVILY_ENDPOINT, json=payload)
        data = res.json()

        cleaned = []
        for item in data.get("results", []):
            cleaned.append({
                "title": item.get("title", ""),
                "url": item.get("url", ""),
                "content": item.get("content", "")
            })

        return cleaned

    except Exception as e:
        print("[TAVILY ERROR]:", e)
        return []
