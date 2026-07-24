# RAG Decision

## Choice: No RAG. Non-RAG context injection.

We load and select markdown directly into the prompt. No embeddings, no vector store.

## Defense

**Corpus size and structure.** The full knowledge base is 6 markdown files: 4 primary (book framework, AI Interaction Map, bio and credentials, past content samples) and 2 secondary (industry trends, competitor positioning). All 6 fit comfortably inside a single prompt's context window with room to spare. There is no scale problem here that retrieval would solve.

**Change frequency.** The primary knowledge base changes rarely. The book framework and bio don't change week to week. The secondary knowledge base (industry trends, competitor positioning) updates more often, but manually and infrequently, on the order of once every few weeks as new reports come out. Static loading handles this fine. Nothing here demands live indexing.

**Query diversity.** This system doesn't answer open-ended questions across a large document library. It generates a narrow, predictable set of outputs: brand-aligned posts, industry-contextual posts, and hybrid posts, from a fixed and small set of source documents. Low query diversity over a small corpus is exactly the case where retrieval adds cost without adding value.

**Context window, cost, and latency.** All 6 files combined are small enough to fit inside a single prompt with no truncation. Stuffing full context costs a bit more per call in tokens, but that cost is trivial at this corpus size, and it avoids the latency and complexity of an extra retrieval step, plus the risk of a retrieval step pulling the wrong chunk out of context.

**Complexity vs. 2-day scope.** Building embeddings and a vector store would add real setup time (chunking strategy, embedding model choice, vector DB setup, retrieval tuning) for a corpus small enough that none of it changes the output quality. That time is better spent on the actual uniqueness strategies: style variation, human review, and prompt iteration, which are the parts of this project that are actually being graded on differentiation.

## What we implemented instead

`knowledge_base.py` loads all markdown files from `knowledge_base/primary/` and `knowledge_base/secondary/` at startup, and selects the most relevant 1-2 primary documents plus 1 secondary document per content request, based on a simple keyword match against the requested topic. The selected documents are inserted into the prompt in full, not as chunks.

## When we would revisit this

If the knowledge base grew past roughly 15-20 documents, or if content requests started needing to search across a large, frequently updated library rather than a small fixed set of source docs, retrieval would start to earn its complexity. At that point a lightweight retrieval step (even without a full vector store, just a smarter selection function) would be worth building before a full embeddings-and-vector-DB setup.