"""
knowledge_base.py

Loads both knowledge bases (via document_processor) and selects
which documents are relevant to a given content topic.

This is the non-RAG context injection step. No embeddings, no
vector store. Selection is done by simple keyword matching against
each document's content. See rag_decision.md for why this is enough
at this corpus size.
"""

from document_processor import load_all_documents


def score_document(document, topic_keywords):
    """
    Count how many topic keywords appear in the document's content.
    Case-insensitive. Higher score = more relevant.
    """
    content_lower = document["content"].lower()
    score = 0

    for keyword in topic_keywords:
        score += content_lower.count(keyword.lower())

    return score


def select_relevant_documents(topic, all_documents, primary_count=2, secondary_count=1):
    """
    Given a topic string, pick the most relevant primary and
    secondary documents based on keyword overlap.

    topic: a short string describing what the content is about,
           e.g. "AI adoption failures in enterprise design"
    all_documents: the dict returned by load_all_documents()
    primary_count: how many primary docs to select
    secondary_count: how many secondary docs to select

    Returns a dict: {"primary": [...], "secondary": [...]}
    """
    topic_keywords = topic.lower().split()

    scored_primary = [
        (score_document(doc, topic_keywords), doc)
        for doc in all_documents["primary"]
    ]
    scored_secondary = [
        (score_document(doc, topic_keywords), doc)
        for doc in all_documents["secondary"]
    ]

    # Sort highest score first
    scored_primary.sort(key=lambda pair: pair[0], reverse=True)
    scored_secondary.sort(key=lambda pair: pair[0], reverse=True)

    selected_primary = [doc for score, doc in scored_primary[:primary_count]]
    selected_secondary = [doc for score, doc in scored_secondary[:secondary_count]]

    # Fallback: if nothing scored above 0, still return the top
    # docs by list order so the pipeline never runs with zero context.
    if not any(score > 0 for score, _ in scored_primary):
        selected_primary = [doc for _, doc in scored_primary[:primary_count]]

    return {
        "primary": selected_primary,
        "secondary": selected_secondary,
    }


def build_context_block(selected_documents):
    """
    Turn selected documents into a single text block ready to
    insert into a prompt. Includes document titles so the model
    knows what it's reading.
    """
    blocks = []

    for doc in selected_documents["primary"] + selected_documents["secondary"]:
        blocks.append(f"### {doc['title']}\n{doc['content']}")

    return "\n\n---\n\n".join(blocks)


if __name__ == "__main__":
    # Manual test: pick a topic, show which documents get selected.
    all_docs = load_all_documents()

    test_topic = "AI adoption failure enterprise trust"
    selected = select_relevant_documents(test_topic, all_docs)

    print(f"Topic: {test_topic}\n")
    print("Selected primary docs:")
    for doc in selected["primary"]:
        print(f"  - {doc['title']}")

    print("Selected secondary docs:")
    for doc in selected["secondary"]:
        print(f"  - {doc['title']}")