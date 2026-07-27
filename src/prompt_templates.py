"""
prompt_templates.py

This file stores prompt templates.

A prompt template is a reusable instruction for the LLM.
Instead of writing a long prompt again and again, we create a Python function
that builds the prompt for us.

Refined per prompt_iteration_log.md and team review: introduces a
Shared Editorial Guidelines block, used by all three templates, that
defines HOW the model should write. Each template still defines WHAT
it should produce, via its own Requirements section.
"""


SHARED_EDITORIAL_GUIDELINES = """
Editorial Guidelines

Before writing:
1. Identify the most relevant target reader.
2. Identify the single most important message.
3. Identify the desired outcome for the reader.

Use the provided context as the primary source of:
- expertise
- consulting experience
- brand perspective
- examples
- terminology

Use general professional knowledge only to explain concepts when necessary, without contradicting or replacing the provided context.

Adapt the depth, terminology and examples to the identified audience while preserving the original meaning of the retrieved context.

Do not copy or closely imitate the wording, sentence structure or organisation of the source material.
Instead, synthesize the information into an original piece adapted to the requested format.

Write for busy professionals.
Prioritize usefulness over completeness.
Every sentence should add value.
Remove repetition and unnecessary introductions.
Avoid explaining everything.

Use active voice.
Prefer concrete examples over abstract explanations.
Keep paragraphs short and easy to scan.
Use white space where appropriate.
Optimize readability for digital consumption.
Maintain a consistent tone throughout the piece.
Avoid AI cliches, corporate buzzwords and exaggerated claims.

Adjust the length to the complexity of the topic unless the selected content type has specific platform constraints.

For quantitative data, metrics, dates, names and factual statements, preserve the original information exactly as provided in the context.

If the retrieved context does not provide enough information, do not invent facts.
Instead, use established professional knowledge only to explain concepts, never to fabricate evidence.
Never invent facts, statistics, client names or unsupported claims.

Before finishing, verify that the conclusion reinforces the core message identified at the beginning.
"""


def thought_leadership(topic: str, context: str) -> str:
    """
    Create a prompt for a thought-leadership content piece.

    Refinement focus: improve audience definition, thesis clarity,
    semantic structure and long-form readability.
    """

    prompt = f"""
You are writing for a personal AI/UX consulting brand.

Write a thought-leadership piece about this topic:
{topic}

Use this brand/context knowledge:
{context}

{SHARED_EDITORIAL_GUIDELINES}

Thought Leadership Requirements
- Present one clear thesis rather than explaining the topic.
- Challenge a misconception, assumption or industry practice.
- Support your reasoning using practical consulting insight from the provided context.
- State the main idea early.
- Build one central argument.
- Acknowledge relevant trade-offs when appropriate.
- Use descriptive section headings when the content is intended for long-form reading.
- Use semantic terminology naturally.
- End with one practical insight, recommendation or rule of thumb.
"""

    return prompt


def linkedin_post(topic: str, context: str) -> str:
    """
    Create a prompt for a LinkedIn post.

    Refinement focus: strengthen transformation narrative, clarify
    actual results vs expected impact, apply shared grounding rules.
    """

    prompt = f"""
You are writing a LinkedIn post for a personal AI/UX consulting brand.

Write about this topic:
{topic}

Use this brand/context knowledge:
{context}

{SHARED_EDITORIAL_GUIDELINES}

LinkedIn Requirements
- Write for mobile-first reading.
- Communicate the main idea before the "See more" break.
- Focus on one professional insight only.
- Open with a genuine hook based on:
  - a misconception,
  - a lesson learned,
  - a professional challenge,
  - or an unexpected observation.
- Use paragraphs of one or two sentences.
- Separate ideas with white space.
- Avoid generic openings.
- Avoid explaining everything.
- Leave the reader with one useful takeaway.
- Finish with the closing that best serves the message:
  - reflection,
  - recommendation,
  - genuine question,
  - or point of view.
- Do not force engagement.
- Target approximately 900-1300 characters while prioritizing clarity over length.
"""

    return prompt


def case_study_summary(topic: str, context: str) -> str:
    """
    Create a prompt for a short case-study summary.

    Refinement focus: strengthen transformation narrative, clarify
    actual results vs expected impact, apply shared grounding rules.
    """

    prompt = f"""
You are writing a short case-study summary for a personal AI/UX consulting brand.

Case study topic:
{topic}

Use this brand/context knowledge:
{context}

{SHARED_EDITORIAL_GUIDELINES}

Write the summary using this structure:

Problem
Describe the user, business or product challenge.

Approach
Explain the strategic intervention and why it was chosen.

Insight
Describe the key learning or design insight.

Result or Potential Impact
Clearly distinguish between actual results and expected impact.

Case Study Requirements
- Present the project as a transformation rather than a chronological task list.
- Prioritize business value and user value.
- Explain why the chosen approach mattered.
- Use only information supported by the provided context.
- Never invent metrics, quotations, client names or results.
- Avoid repeating information across sections.
- Make the most important outcome immediately visible.
- Keep the summary concise, credible and easy to scan.
"""

    return prompt