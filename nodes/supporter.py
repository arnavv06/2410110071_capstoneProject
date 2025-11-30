import json
import os
from dotenv import load_dotenv
from openai import OpenAI

from state.debateState import DebateState
from tools.assignTools import TOOLS
from tools.searchTool import search_tavily
from tools.wikipediaTool import wikipedia_search
from tools.newsSummaryTool import summarize_news
from tools.topicClassifierTool import classify_topic

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1100,
            temperature=0.2
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[Supporter LLM ERROR]:", e)
        return "{}"


def load_supporter_prompt():
    with open("prompts/supporterPrompt.txt", "r", encoding="utf-8") as f:
        return f.read()


def run_tool(tool_name: str, claim: str, tavily_cache=None):

    if tool_name == "tavily":
        return search_tavily(claim)

    elif tool_name == "wikipedia":
        return wikipedia_search(claim)

    elif tool_name == "news_summary":
        
        return summarize_news(tavily_cache or [])

    elif tool_name == "topic_classifier":
        return classify_topic(claim)

    else:
        return None


def supporter_node(state: DebateState) -> DebateState:
    """Supporter automatically loops through tools listed in registry."""

    claim = state["claim"]
    tool_list = TOOLS["supporter"]

    combined_docs = {}
    tavily_cache = None

    # Loop through tools dynamically
    for tool in tool_list:
        result = run_tool(tool, claim, tavily_cache)

        if tool == "tavily":
            tavily_cache = result

        combined_docs[tool] = result

    state["retrieved_docs"] = combined_docs

    # Fill prompt
    prompt_template = load_supporter_prompt()
    filled_prompt = (
        prompt_template
        .replace("{{claim}}", claim)
        .replace("{{context}}", str(state.get("context")))
        .replace("{{retrieved_docs}}", json.dumps(combined_docs, indent=2))
    )

    response_text = call_llm(filled_prompt)

    try:
        supporter_output = json.loads(response_text)
    except json.JSONDecodeError:
        supporter_output = {"pros": []}

    state["supporter_output"] = supporter_output
    return state
