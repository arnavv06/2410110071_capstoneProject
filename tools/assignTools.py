# tools/toolsRegistry.py
"""
toolsRegistry.py
----------------
Central registry of all tools available to each agent.
Supporter and Critic automatically loop through this registry
to gather evidence from multiple tools in a modular way.
"""

TOOLS = {
    "supporter": [
        "tavily",
        "wikipedia",
        "news_summary",
        "topic_classifier"
    ],

    "critic": [
        "tavily",
        "wikipedia",
        "news_summary",
        "topic_classifier"
    ],

    # Judge ONLY uses RAG fallacy rules
    "judge": [
        "rag_rules"
    ]
}
