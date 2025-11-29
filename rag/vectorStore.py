"""
Builds and manages the vector database for RAG.
Uses ChromaDB PersistentClient for local vector storage (new API).
"""

import json
import os
from typing import List, Dict, Any

from chromadb import PersistentClient
from chromadb.utils import embedding_functions


class DebateVectorStore:
    """
    Wrapper around ChromaDB using the new PersistentClient interface.
    """

    def __init__(
        self,
        persist_directory: str = "data/processed/vectorstore",
        collection_name: str = "debate_rules_chunks",
        embedding_model: str = "all-MiniLM-L6-v2"
    ):

        self.persist_directory = persist_directory
        self.collection_name = collection_name

        # Ensure directory exists
        os.makedirs(persist_directory, exist_ok=True)

        # New Chroma client syntax
        self.client = PersistentClient(path=persist_directory)

        # Embedding function (SentenceTransformer)
        self.embedding_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name=embedding_model
        )

        # Load or create the collection
        try:
            self.collection = self.client.get_collection(name=collection_name)
        except:
            self.collection = self.client.create_collection(
                name=collection_name,
                embedding_function=self.embedding_fn
            )

    # ----------------------------------------------------------------------
    def add_chunks(self, chunks: List[Dict[str, str]]) -> None:
        """Adds chunks to vectorstore."""

        ids = [chunk["id"] for chunk in chunks]
        texts = [chunk["text"] for chunk in chunks]

        self.collection.add(
            ids=ids,
            documents=texts
        )

    # ----------------------------------------------------------------------
    def query(self, query_text: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Performs similarity search."""

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        retrieved = []
        for i in range(len(results["ids"][0])):
            retrieved.append({
                "id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "distance": results["distances"][0][i]
            })

        return retrieved

    # ----------------------------------------------------------------------
    def load_chunks_from_json(self, path: str = "data/processed/chunks.json") -> List[Dict[str, str]]:
        """Load chunks.json."""
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


# ====================
#  MAIN EXECUTION
# ====================
def main():
    """
    Build vectorstore from chunks.json.
    """

    chunks_path = "data/processed/chunks.json"
    vectorstore_dir = "data/processed/vectorstore"

    if not os.path.exists(chunks_path):
        raise FileNotFoundError("❌ chunks.json missing! Run chunker.py first.")

    with open(chunks_path, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    vs = DebateVectorStore(persist_directory=vectorstore_dir)

    vs.add_chunks(chunks)

    print(" Built vector store succesfuuly")


if __name__ == "__main__":
    main()
 