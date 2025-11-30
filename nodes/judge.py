# nodes/judge.py
"""
Judge Node
----------
Retrieves relevant fallacy/rule chunks using RAG,
loads judge prompt, calls OpenAI,
parses JSON, updates final verdict.
"""

import json
import os

from dotenv import load_dotenv
load_dotenv()

from openai import OpenAI
from state.debateState import DebateState
from rag.retrieval import retrieve_relevant_rules

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def call_llm(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1500,
            temperature=0.0  
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("[Judge LLM ERROR]:", e)
        return "{}"


def load_judge_prompt() -> str:
    with open("prompts/judgePrompt.txt", "r", encoding="utf-8") as f:
        return f.read()


def judge_node(state: DebateState) -> DebateState:
    """Main Judge logic."""

    # (RAG)
    rag_snippets = retrieve_relevant_rules(state["claim"], top_k=5)
    state["retrieved_docs"] = rag_snippets


    prompt_template = load_judge_prompt()

    filled_prompt = (
        prompt_template
        .replace("{{claim}}", state["claim"])
        .replace("{{context}}", str(state.get("context")))
        .replace("{{supporter_output}}", json.dumps(state.get("supporter_output", {}), indent=2))
        .replace("{{critic_output}}", json.dumps(state.get("critic_output", {}), indent=2))
        .replace("{{retrieved_docs}}", json.dumps(rag_snippets, indent=2))
    )

    response_text = call_llm(filled_prompt)

    try:
        verdict = json.loads(response_text)
    except json.JSONDecodeError:
        verdict = {"final_recommendation": "Undecided", "confidence": 0}

    state["final_verdict"] = verdict
    return state
