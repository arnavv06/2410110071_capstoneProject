from typing import TypedDict, Optional, Dict, List, Any


class DebateState(TypedDict, total=False):
    """
    Represents the complete state passed along the pipeline.
    Fields are optional because at the beginning, only `claim` is present.
    """

    # claim input
    claim: str      
    context: Optional[str]

    # Node outputs
    supporter_output: Dict[str, Any]
    critic_output: Dict[str, Any]

    # RAG documents retrieved for Judge
    retrieved_docs: List[Dict[str, Any]]

    # Judge writes final output to this
    final_verdict: Dict[str, Any]


def initialize_state(claim: str, context: Optional[str] = None) -> DebateState:
    """
    Creates the initial LangGraph state.
    Only `claim` and `context` are filled; everything else will be populated later.
    """
    return {
        "claim": claim,
        "context": context,
        "supporter_output": {},
        "critic_output": {},
        "retrieved_docs": [],
        "final_verdict": {},
    }
