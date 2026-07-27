"""
document_processor.py

Reads markdown files from the knowledge base folders and returns
their content as plain text, along with basic metadata (filename,
title, folder). This is the ingestion step of the pipeline:
document -> monitor -> brief -> publish -> iterate.

No RAG here. Files are read in full. See rag_decision.md for why.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
PRIMARY_DIR = BASE_DIR / "knowledge_base" / "primary"
SECONDARY_DIR = BASE_DIR / "knowledge_base" / "secondary"

def read_markdown_file(filepath):
    """
    Read a single markdown file and return its raw text content.
    Returns None if the file doesn't exist or can't be read.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        return None
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
        return None


def get_title_from_content(content):
    """
    Pull the first markdown heading (# Title) from the file content
    to use as a readable title. Falls back to 'Untitled' if none found.
    """
    for line in content.splitlines():
        if line.startswith("# "):
            return line.replace("# ", "").strip()
    return "Untitled"


def load_folder(folder_path):
    """
    Read every .md file in a folder and return a list of documents.
    Each document is a dict: filename, title, folder, content.
    """
    documents = []

    if not folder_path.exists():
        print(f"Folder not found: {folder_path}")
        return documents

    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".md"):
            continue

        filepath = folder_path / filename
        content = read_markdown_file(filepath)

        if content is None:
            continue

        documents.append({
            "filename": filename,
            "title": get_title_from_content(content),
            "folder": folder_path.name,
            "content": content,
        })

    return documents


def load_all_documents():
    """
    Load both knowledge bases. Returns a dict with two keys:
    'primary' and 'secondary', each a list of document dicts.
    """
    return {
        "primary": load_folder(PRIMARY_DIR),
        "secondary": load_folder(SECONDARY_DIR),
    }


if __name__ == "__main__":
    # Quick manual test: run this file directly to confirm
    # both knowledge bases load correctly.
    docs = load_all_documents()

    print(f"Primary documents loaded: {len(docs['primary'])}")
    for doc in docs["primary"]:
        print(f"  - {doc['filename']} ({doc['title']})")

    print(f"Secondary documents loaded: {len(docs['secondary'])}")
    for doc in docs["secondary"]:
        print(f"  - {doc['filename']} ({doc['title']})")