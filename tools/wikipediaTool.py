# tools/wikipedia_tool.py
"""
Wikipedia Summary Tool
----------------------
Returns the summary paragraph of a Wikipedia page.
"""

import requests

WIKI_ENDPOINT = "https://en.wikipedia.org/api/rest_v1/page/summary/"


def wikipedia_search(topic: str) -> dict:
    topic = topic.replace(" ", "_")

    try:
        res = requests.get(WIKI_ENDPOINT + topic, timeout=6)
        if res.status_code != 200:
            return {}

        data = res.json()

        return {
            "title": data.get("title", ""),
            "extract": data.get("extract", ""),
            "url": data.get("content_urls", {}).get("desktop", {}).get("page", "")
        }

    except Exception as e:
        print("[WIKIPEDIA ERROR]:", e)
        return {}
