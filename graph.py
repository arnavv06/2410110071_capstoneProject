"""
graph.py
Defines the LangGraph pipeline for the Multi-Agent Debate Decision Advisor.

Graph flow:
    supporter → critic → judge → END

The graph takes an initial DebateState (claim, context),
runs each agent node in sequence, and outputs final_verdict.
"""

from langgraph.graph import StateGraph, END
from state.debateState import DebateState
from nodes.supporter import supporter_node
from nodes.critic import critic_node
from nodes.judge import judge_node


def build_graph() -> StateGraph:
    """
    Builds and returns the LangGraph StateGraph for the debate system.
    """

    #graph with DebateState as the state
    graph = StateGraph(DebateState)

    # add nodes
    graph.add_node("supporter", supporter_node)
    graph.add_node("critic", critic_node)
    graph.add_node("judge", judge_node)

    # add edges
    graph.add_edge("supporter", "critic")
    graph.add_edge("critic", "judge")
    graph.add_edge("judge", END)

    # 4. Set start and end nodes
    graph.set_entry_point("supporter")

    # compile graph to object
    return graph.compile()


def run_debate(claim: str, context: str = None):
    """
    Creates initial state, runs the graph, returns the final verdict.
    Returns:
        dict: The judge's final verdict JSON.
    """

    from state.debateState import initialize_state

    state = initialize_state(claim=claim, context=context)

    graph = build_graph()

    final_state = graph.invoke(state) #run

    return final_state.get("final_verdict", {})
