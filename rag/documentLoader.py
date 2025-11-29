"""
Loads the debate-rules PDF from data/raw/ and extracts clean text,
then saves it to data/processed/raw_text.txt
"""

import os
from pypdf import PdfReader


def load_pdf_text(filepath: str) -> str:
    """
    Extract text from PDF, clean whitespace, return as string.
    """
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"PDF file not found: {filepath}")

    reader = PdfReader(filepath)
    all_text = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            cleaned = " ".join(text.split())  # remove awkward spacing
            all_text.append(cleaned)

    return "\n".join(all_text)


def main():
    """
    Load debate_rules.pdf and save raw_text.txt into data/processed/.
    """
    input_path = os.path.join("data", "raw", "debate_rules.pdf")
    output_dir = os.path.join("data", "processed")
    output_path = os.path.join(output_dir, "raw_text.txt")

    os.makedirs(output_dir, exist_ok=True)

    text = load_pdf_text(input_path)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(text)

    print("PDF extraction complete")


if __name__ == "__main__":
    main()
