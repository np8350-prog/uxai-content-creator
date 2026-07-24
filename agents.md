# Agents.md — VSCode Agent Configuration

This documents how we configured and used the VSCode agent for this project, per the brief's requirement to set up and document agent workflow.

## Setup

1. Open the repo in VSCode
2. Install the Codex extension (OpenAI Codex for VSCode)
3. Sign in / authenticate with the API key
4. Point the agent at the repo root so it has visibility into `src/`, `knowledge_base/`, and `templates/`
5. Config file: `config/vscode_agent.json` holds the agent's working rules for this project (see below)

**Note:** this file documents our agreed rules for using Codex. Codex does not automatically read or enforce this config, the team follows these rules manually and reviews agent output against them.

## `config/vscode_agent.json` (what it should contain)

- Which folders the agent should treat as context (`src/`, `knowledge_base/`)
- Which folders the agent should never write to (`knowledge_base/primary/`, since that's source-of-truth brand material, not generated output)
- Preferred coding style: Python, PEP8, functions over classes unless state genuinely needs to persist

## How we used the agent during the project

- Scaffolding: generating boilerplate for each pipeline stage file, then hand-editing
- Debugging: pasting error output back to the agent for a first-pass fix, verifying manually before accepting
- Not used for: the actual prompt template wording, human review logic, or anything tied to uniqueness. Those stayed human-written and human-reviewed, on purpose, since agent-generated prompt copy would undercut the project's own uniqueness argument.

## Team workflow rule

Each teammate ran the agent locally against their own stage (Document/KB, LLM/Prompts, Pipeline/Evidence). No shared agent session. Code was still reviewed by a teammate before merging, agent-assisted or not.