# UXAI Content Creator

An AI content creation system that generates brand-aligned, contextually unique content for a real AI/UX consulting personal brand. Built for Project 2 (IronHack, Module 2).

Generates content across three formats (Thought Leadership, LinkedIn Post, Case Study Summary), grounded in two markdown knowledge bases, with human review built into the pipeline at every step.

## What makes this different from generic AI content

- Two real knowledge bases (brand + industry research), injected directly into every prompt
- Non-RAG context selection (see `rag_decision.md` for the full defense)
- Three genuinely different prompt templates, not one template reworded three ways
- A human review checkpoint on every draft: approve, request edits, or reject
- Every review decision is logged permanently to `uniqueness_evidence/review_log.md`
- Documented, tested prompt iteration, including a caught-and-fixed bug where the system was inventing fake client outcomes (see `prompt_iteration_log.md`)

## Setup

1. Clone the repo and move into it:

        git clone https://github.com/np8350-prog/uxai-content-creator.git
        cd uxai-content-creator

2. Install dependencies:

        pip install -r requirements.txt

   If `pip` doesn't resolve to the right Python on your machine, use:

        python3 -m pip install -r requirements.txt

3. Add your own API key. Create a `.env` file in the repo root:

        touch .env

   Add this line, with your own key:

        OPENAI_API_KEY=your_key_here

   `.env` is gitignored and never committed. Each teammate needs their own.

## Running it

There are two interfaces, both use the exact same underlying pipeline.

### Web app (recommended)

    cd src
    python3 app.py

Then open `http://127.0.0.1:5000` in a browser.

Flow: enter a topic, choose a content type, wait for generation (loading screen shows real pipeline stages), review the draft, including an automatic quality check for LinkedIn posts, then Approve, Request edits (loops back with your feedback and regenerates), or Reject (offers several next steps). Every decision is logged and viewable at `/log` (the "History" link in the top bar). Approved content can be downloaded as a `.txt` file.

### Command line

    cd src
    python3 main.py

Same pipeline, terminal-based prompts instead of a browser.

## Project structure

    uxai-content-creator/
    ├── src/
    │   ├── document_processor.py   # Reads markdown files from both knowledge bases
    │   ├── knowledge_base.py       # Scores and selects relevant docs per topic
    │   ├── prompt_templates.py     # 3 content templates + shared editorial guidelines
    │   ├── llm_integration.py      # OpenAI API call
    │   ├── content_pipeline.py     # Wires the above into one generation/revision flow
    │   ├── review.py               # Human review checkpoint + decision logging
    │   ├── content_checker.py      # Automatic LinkedIn post quality checks
    │   ├── main.py                 # CLI entry point
    │   ├── app.py                  # Flask web app entry point
    │   ├── templates/              # HTML templates for the web app
    │   ├── static/style.css        # Web app styling
    │   └── test_*.py               # Manual test scripts per template/component
    ├── knowledge_base/
    │   ├── primary/                # Brand-specific: book framework, AI Interaction Map, bio/credentials, past content samples
    │   └── secondary/              # Industry research: trends, competitor positioning
    ├── uniqueness_evidence/
    │   ├── review_log.md           # Every real human review decision, logged automatically
    │   ├── style_variation.md      # Same topic across all 3 templates, compared
    │   └── chatgpt_comparison.md   # Our system vs. plain ChatGPT, same topic
    ├── config/vscode_agent.json    # Documented agent configuration
    ├── agents.md                   # How the VSCode agent (Codex) was used and constrained
    ├── rag_decision.md             # RAG vs. non-RAG decision and defense
    ├── prompt_iteration_log.md     # Prompt evaluation, refinements, confirmed before/after
    ├── project_structure.md        # Team roles, MVP scope, deliverables checklist
    └── requirements.txt

## Tech stack

- Python 3
- OpenAI API (`openai` SDK)
- Flask (web interface)
- Markdown knowledge base, no vector store (see `rag_decision.md`)
- VSCode + Codex for scaffolding and debugging only, never for prompt wording or review logic (see `agents.md`)

## Key documents for grading

- RAG decision + defense: `rag_decision.md`
- Prompt iteration evidence: `prompt_iteration_log.md`
- Uniqueness evidence: `uniqueness_evidence/`
- Agent configuration: `agents.md`, `config/vscode_agent.json`