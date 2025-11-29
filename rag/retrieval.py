# rag/retrieval.py
"""
retrieval.py
High-level retrieval helpers that wrap DebateVectorStore for the Judge (and Critic).
Provide functions to:
 - initialize/load the vector store
 - ingest chunks (if needed)
 - retrieve top-k relevant chunks for a query or list of queries
"""

from typing import List, Dict, Any, Optional
import os

from rag.vectorStore import DebateVectorStore


# Keep a module-level cache so we don't re-create the client repeatedly.
_STORE_CACHE: Optional[DebateVectorStore] = None


def init_or_get_store(
    persist_directory: str = "data/processed/vectorstore",
    collection_name: str = "debate_rules_chunks",
    embedding_model: str = "all-MiniLM-L6-v2",
) -> DebateVectorStore:
    """
    Initialize and return a DebateVectorStore instance. Uses a module-level cache
    so repeated calls return the same instance.

    Args:
        persist_directory: directory where chroma persists data
        collection_name: chroma collection name
        embedding_model: sentence-transformers model name used internally

    Returns:
        DebateVectorStore: initialized vector store wrapper
    """
    global _STORE_CACHE
    if _STORE_CACHE is None:
        _STORE_CACHE = DebateVectorStore(
            persist_directory=persist_directory,
            collection_name=collection_name,
            embedding_model=embedding_model,
        )
    return _STORE_CACHE


def ingest_chunks_if_needed(
    store: DebateVectorStore,
    chunks_json_path: str = "data/processed/chunks.json",
    force: bool = False,
) -> None:
    """
    Load chunks from a JSON file and add them to the store if the collection appears empty
    or if force=True. This is a convenient helper for notebooks and scripts.

    Args:
        store: DebateVectorStore instance
        chunks_json_path: path to precomputed chunks.json
        force: if True, always (re)ingest chunks
    """
    # Very small heuristic: if collection is empty (no ids) or force is set, ingest.
    try:
        # Try a lightweight query to check existence. If there are no items,
        # collection.query may return empty lists.
        existing = store.query("test", n_results=1)
        should_ingest = force or (len(existing) == 0)
    except Exception:
        # If anything goes wrong (e.g., empty DB), set to ingest
        should_ingest = True

    if should_ingest:
        if not os.path.exists(chunks_json_path):
            raise FileNotFoundError(f"Chunks JSON not found: {chunks_json_path}")
        chunks = store.load_chunks_from_json(chunks_json_path)
        store.add_chunks(chunks)


def retrieve_relevant_rules(query_text: str, top_k: int = 5) -> List[Dict[str, Any]]:
    """
    Retrieve the top_k most relevant chunks for a single query.

    Args:
        query_text: the textual query (e.g., an argument, or "strawman fallacy")
        top_k: number of results to return

    Returns:
        List[Dict[str, Any]]: list of dicts with keys: id, text, distance
    """
    store = init_or_get_store()
    # Ensure data exists; don't force re-ingest by default.
    ingest_chunks_if_needed(store, chunks_json_path="data/processed/chunks.json", force=False)
    return store.query(query_text, n_results=top_k)


def batch_retrieve_for_arguments(
    texts: List[str], top_k: int = 3
) -> List[List[Dict[str, Any]]]:
    """
    For a list of argument texts, retrieve top_k relevant chunks for each one.

    Args:
        texts: list of strings (e.g., supporter argument texts)
        top_k: top-k chunks per text

    Returns:
        List[List[Dict[str, Any]]]: outer list aligns with input texts; each element
        is a list of retrieved chunk dicts for that text.
    """
    store = init_or_get_store()
    ingest_chunks_if_needed(store, chunks_json_path="data/processed/chunks.json", force=False)

    grouped_results: List[List[Dict[str, Any]]] = []
    for t in texts:
        snippets = store.query(t, n_results=top_k)
        grouped_results.append(snippets)
    return grouped_results
