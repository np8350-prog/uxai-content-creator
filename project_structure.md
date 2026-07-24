# Project Structure: uxai-content-creator

## One-sentence description

An AI content creation system that generates brand-aligned, contextually unique content for an AI/UX consulting personal brand, using two markdown knowledge bases and non-RAG context injection to avoid generic AI output.

## What we're building

A Python pipeline that takes a content topic, pulls relevant context from two knowledge bases (personal brand material, and industry/competitor research), and generates content through the LLM API using prompt templates built for style variation. Content stops for human review before anything is considered "done." We prove the output is different from generic ChatGPT by comparing outputs side by side.

## Idea and company

Idea 2: Personal Brand Content Creator. The brand is Nelly's real AI/UX consulting practice. Real materials, not a fictional company.

## Team roles (draft, confirm with group)

- **Person 1:** Kanban board owner, tracks card movement, screenshots
- **Person 2:** [fill in]
- **Person 3:** [fill in]

Suggested split by pipeline stage, not by person doing "everything":
- Document processing + knowledge base loading
- LLM integration + prompt templates
- Content pipeline orchestration + uniqueness evidence (human review log, style variation comparison, ChatGPT comparison)

## RAG decision

No RAG. Non-RAG context injection. See `rag_decision.md` for the full defense.

## Knowledge bases (already built)

Primary: `book_framework.md`, `ai_interaction_map.md`, `bio_credentials.md`, `past_content_samples.md`
Secondary: `industry_trends.md`, `competitor_positioning.md`

## MVP scope

Document → load and select knowledge base context → generate content via prompt template → human review checkpoint → output.

## Uniqueness strategies (must produce evidence, not just design intent)

1. Human in the Loop: review checkpoint + review log
2. Style Variation: 3 distinct prompt templates
3. Contextual Placement: knowledge base selection function, named concepts in prompts
4. Iterative Prompt Engineering: prompt iteration log

## Deliverables checklist

- [ ] GitHub repo with working pipeline
- [ ] rag_decision.md
- [ ] README with setup instructions
- [ ] agents.md (VSCode agent config)
- [ ] Uniqueness evidence folder (review log, style comparison, ChatGPT comparison, prompt iteration log)
- [ ] Kanban board, Day 1 and Day 2 screenshots
- [ ] Presentation