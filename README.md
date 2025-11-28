# Overview of MAT496

In this course, we have primarily learned Langgraph. This is helpful tool to build apps which can process unstructured `text`, find information we are looking for, and present the format we choose. Some specific topics we have covered are:

- Prompting
- Structured Output
- Semantic Search
- Retrieval Augmented Generation (RAG)
- Tool calling LLMs & MCP
- Langgraph: State, Nodes, Graph

We also learned that Langsmith is a nice tool for debugging Langgraph codes.

---

## Title: Multi-Agent Debate Decision Advisor

## Overview

**Multi-Agent Debate Decision Advisor** is an **AI-Powered,** **LangGraph** based system used to help users reach well-reasoned decisions by producing a structured debate between three AI agents. When the user enters a claim, the **Supporter** argues in its favour, the **Critic** challenges it through counter-arguments, and the **Judge** evaluates both sides using RAG over a *logical fallacies* or *debate rules* or some other document. The Judge then provides a structured verdict summarising the pros, cons, and a final recommendation with a confidence score. The project demonstrates how multi-agent reasoning, retrieval, and structured prompting can be combined to reach a balanced decision and achieve critical thinking.

## Reason for picking up this project

* Seemed cool

 includes every key topic taught in the MAT496 course in a meaningful way:

* **Prompting:** Uses prompts for the Supporter, Critic, and Judge agents.
* **Structured Output:** Produces a consistent JSON “Verdict” with pros, cons, and recommendations.
* **Semantic Search:** Retrieves relevant information to support or counter the user’s claim.
* **Retrieval Augmented Generation (RAG):** Judge agent uses a fallacy/rules document to evaluate arguments.
* **Tool Calling:** Supporter and Critic call search tools to gather external evidence.
* **LangGraph (State, Nodes, Graph):** Entire debate flows through a multi-agent LangGraph pipeline.

## Plan

I plan to execute these steps to complete my project.

* [TODO]  **Step 1: Prompt Design**
  * involves writing simple prompts for the three agents (Optimist, Skeptic, Judge) so they behave consistently in the debate.
* **[TODO] Step 2: Prepare RAG material**
  * involves preparing the RAG material by providing debate-rules/fallacies document and breaking it into chunks.
* **[TODO] Step 3: Build the Vector Store**
  * involves creating embeddings for those chunks and storing them in a small vector database for retrieval.
* **[TODO ] Step 4: Setup LangGraph State**
  * involves defining a basic LangGraph state to hold the claim, the arguments generated, and the final verdict.
* **[TODO] Step 5: Implement the Supporter Node**
  * involves building the Supporter node, which searches for supportive evidence and generates pro-arguments.
* **[TODO] Step 6: Implement the Critic Node**
  * involves building the Critic node, which finds counter-evidence and produces opposing arguments.
* **[TODO] Step 7: Implement the Judge Node**
  * involves building the Judge node, which uses RAG to check arguments against debate rules and outputs the structured verdict.
* **[TODO] Step 8: Build the Multi-Agent Graph**
  * involves connecting all three nodes into a single LangGraph pipeline so the debate flows from one agent to the next.
* **[TODO] Step 9: Run a demo**
  * involves making a small demo where the user enters a claim and sees the final decision report.
* **[TODO] Step 10: Final Documentation & Testing**
  * involves final polishing: documentation, sample outputs testing etc.

## Conclusion:

To be filled upon completion.

---
