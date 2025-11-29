"""
Splits the debate-rules text into clean, overlapping chunks for embedding.
This file defines a simple, reliable character-based chunker.
"""

import os
import json
from typing import List, Dict


def chunk_text(text: str, chunk_size: int = 700, overlap: int = 150) -> List[Dict[str, str]]:
    """
    Splits the input text into overlapping chunks.
    """

    chunks = []
    start = 0
    chunk_id = 0

    # Normalize whitespace
    text = " ".join(text.split())

    while start < len(text):
        end = start + chunk_size
        chunk_content = text[start:end]

        chunks.append({
            "id": f"chunk_{chunk_id}",
            "text": chunk_content
        })

        chunk_id += 1
        start += (chunk_size - overlap)

    return chunks


def save_chunks_to_json(chunks: List[Dict[str, str]], output_path: str) -> None:
    """ Save chunks list into a JSON file. """
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunks, f, indent=2, ensure_ascii=False)


def process_and_save_chunks(raw_text: str,
                            output_path: str = "data/processed/chunks.json",
                            chunk_size: int = 700,
                            overlap: int = 150) -> List[Dict[str, str]]:

    chunks = chunk_text(
        text=raw_text,
        chunk_size=chunk_size,
        overlap=overlap
    )

    save_chunks_to_json(chunks, output_path)
    return chunks


def main():
    """Loads raw_text.txt and creates chunks.json"""
    input_path = os.path.join("data", "processed", "raw_text.txt")
    output_path = os.path.join("data", "processed", "chunks.json")

    if not os.path.exists(input_path):
        raise FileNotFoundError(f"raw_text.txt not found at {input_path}. Run documentLoader.py first.")

    with open(input_path, "r", encoding="utf-8") as f:
        raw_text = f.read()

    chunks = process_and_save_chunks(raw_text, output_path)

    print(f" Saved chunks to: {output_path}")


if __name__ == "__main__":
    main()
