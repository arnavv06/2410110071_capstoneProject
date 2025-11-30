# tools/topic_classifier_tool.py
"""
Topic Classifier Tool
---------------------
Classifies a claim into topic categories like:
technology, science, economics, politics, environment, ethics, education, health.
"""

import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def classify_topic(text: str) -> str:
    """
    Classifies a claim into one topic area.

    Returns:
        str: topic label
    """

    prompt = f"""
    Classify the following claim into one topic category:
    [technology, science, economics, politics, environment, ethics, education, health].

    Claim: {text}

    Return ONLY the topic word.
    """

    try:
        resp = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=10,
            temperature=0.0,
        )
        return resp.choices[0].message.content.strip()

    except Exception as e:
        print("[TOPIC CLASSIFIER ERROR]:", e)
        return "unknown"
