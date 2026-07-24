"""
prompt_templates.py

This file stores prompt templates.

A prompt template is a reusable instruction for the LLM.
Instead of writing a long prompt again and again, we create a Python function
that builds the prompt for us.
"""


def thought_leadership(topic: str, context: str) -> str:
    """
    Create a prompt for a thought-leadership content piece.

    Parameters:
        topic:
            The main idea we want the content to be about.

        context:
            The brand knowledge or selected knowledge-base text
            that should guide the LLM.

    Returns:
        A complete prompt string that can be sent to the LLM.
    """

    prompt = f"""
You are writing for a personal AI/UX consulting brand.

Write a thought-leadership piece about this topic:
{topic}

Use this brand/context knowledge:
{context}

Requirements:
- Write with a clear point of view.
- Make it practical and useful.
- Avoid generic AI hype.
- Sound human, thoughtful, and brand-aligned.
"""

    return prompt

def linkedin_post(topic: str, context: str) -> str:
    """
    Create a prompt for a LinkedIn post.

    Parameters:
        topic:
            The main idea for the LinkedIn post.

        context:
            The brand knowledge or selected knowledge-base text
            that should guide the LLM.

    Returns:
        A complete prompt string written for LinkedIn-style content.
    """

    prompt = f"""
You are writing a LinkedIn post for a personal AI/UX consulting brand.

Write about this topic:
{topic}

Use this brand/context knowledge:
{context}

Requirements:
- Keep it concise and easy to read.
- Use a human, professional voice.
- Make the first line interesting.
- Avoid generic AI buzzwords.
- End with a thoughtful question for the reader.
"""

    return prompt

def case_study_summary(topic: str, context: str) -> str:
    """
    Create a prompt for a short case-study summary.

    Parameters:
        topic:
            The project, problem, or idea the case study should focus on.

        context:
            The brand knowledge or selected knowledge-base text
            that should guide the LLM.

    Returns:
        A complete prompt string that asks the LLM to write
        a structured case-study summary.
    """

    prompt = f"""
You are writing a short case-study summary for a personal AI/UX consulting brand.

Case study topic:
{topic}

Use this brand/context knowledge:
{context}

Write the summary using this structure:

Problem:
Describe the user, business, or product problem.

Approach:
Describe how AI strategy, UX research, or human-centered design helped.

Insight:
Explain the key learning or design insight.

Result or potential impact:
Describe the outcome, benefit, or likely improvement.

Requirements:
- Keep it clear and practical.
- Do not invent fake client names.
- Do not invent fake statistics.
- Use a professional consulting tone.
"""

    return prompt