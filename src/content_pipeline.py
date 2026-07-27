"""
content_pipeline.py

This module manages content generation and revision.

Workflow:
1. Load documents from the knowledge base.
2. Select relevant documents.
3. Build the context block.
4. Create the appropriate prompt.
5. Generate or revise content.
6. Run the LinkedIn checker when applicable.
7. Return the complete pipeline result.
"""

from typing import Optional
from knowledge_base import (
    load_all_documents,
    select_relevant_documents,
    build_context_block,
)

from prompt_templates import (
    thought_leadership,
    linkedin_post,
    case_study_summary,
)

from llm_integration import generate_content
from content_checker import check_linkedin_post


SUPPORTED_CONTENT_TYPES = {
    "thought_leadership",
    "linkedin_post",
    "case_study_summary",
}


def validate_inputs(topic: str, content_type: str) -> None:
    """
    Validate the main pipeline inputs.

    Parameters
    ----------
    topic : str
        Topic requested by the user.

    content_type : str
        Selected content format.

    Raises
    ------
    ValueError
        If the topic is empty or the content type is unsupported.
    """

    if not topic or not topic.strip():
        raise ValueError("The topic cannot be empty.")

    if content_type not in SUPPORTED_CONTENT_TYPES:
        raise ValueError(
            f"Unsupported content type: {content_type}"
        )


def build_generation_prompt(
    topic: str,
    content_type: str,
    context: str,
) -> str:
    """
    Build the original generation prompt.

    Parameters
    ----------
    topic : str
        Content topic.

    content_type : str
        Requested content format.

    context : str
        Knowledge-base context.

    Returns
    -------
    str
        Complete prompt for the LLM.
    """

    if content_type == "thought_leadership":
        return thought_leadership(
            topic=topic,
            context=context,
        )

    if content_type == "linkedin_post":
        return linkedin_post(
            topic=topic,
            context=context,
        )

    if content_type == "case_study_summary":
        return case_study_summary(
            topic=topic,
            context=context,
        )

    raise ValueError(
        f"Unsupported content type: {content_type}"
    )


def build_revision_prompt(
    topic: str,
    content_type: str,
    context: str,
    current_content: str,
    feedback: str,
) -> str:
    """
    Build a prompt that revises an existing draft.

    Parameters
    ----------
    topic : str
        Original topic.

    content_type : str
        Original content format.

    context : str
        Knowledge-base context.

    current_content : str
        Draft that needs revision.

    feedback : str
        Human reviewer feedback.

    Returns
    -------
    str
        Complete revision prompt.
    """

    if not current_content or not current_content.strip():
        raise ValueError(
            "Current content is required for a revision."
        )

    if not feedback or not feedback.strip():
        raise ValueError(
            "Reviewer feedback cannot be empty."
        )

    return f"""
You are revising an existing piece of content.

TOPIC:
{topic}

CONTENT TYPE:
{content_type}

KNOWLEDGE-BASE CONTEXT:
{context}

CURRENT DRAFT:
{current_content}

HUMAN REVIEWER FEEDBACK:
{feedback}

Revise the draft according to the reviewer feedback.

Requirements:
- Preserve the original topic and content type.
- Use the supplied knowledge-base context.
- Apply the requested changes clearly.
- Keep accurate and relevant information.
- Do not explain what you changed.
- Return only the revised content.
""".strip()


def run_content_checker(
    generated_content: str,
    content_type: str,
):
    """
    Run the relevant automatic quality checker.

    The existing checker only applies to LinkedIn posts.

    Parameters
    ----------
    generated_content : str
        Generated or revised draft.

    content_type : str
        Selected content format.

    Returns
    -------
    Optional[dict]
        Checker results for LinkedIn posts, otherwise None.
    """

    if content_type == "linkedin_post":
        return check_linkedin_post(generated_content)

    return None


def generate_content_pipeline(
    topic: str,
    content_type: str,
    current_content: Optional[str] = None,
    feedback: Optional[str] = None,
) -> dict:
    """
    Generate a new draft or revise an existing draft.

    To generate a new draft:
        provide topic and content_type.

    To revise a draft:
        also provide current_content and feedback.

    Parameters
    ----------
    topic : str
        Topic requested by the user.

    content_type : str
        Requested content format.

    current_content : Optional[str]
        Existing draft when a revision is requested.

    feedback : Optional[str]
        Human reviewer feedback.

    Returns
    -------
    dict
        Pipeline result containing:
        - generated_content
        - selected_documents
        - context
        - checker_results
        - generation_mode
    """

    validate_inputs(topic, content_type)

    # Load documents from the project knowledge base.
    all_documents = load_all_documents()

    # Select the documents most relevant to the topic.
    selected_documents = select_relevant_documents(
        topic,
        all_documents,
    )

    # Combine the selected documents into one context block.
    context = build_context_block(selected_documents)

    # A revision requires both current content and feedback.
    revision_requested = (
        current_content is not None
        or feedback is not None
    )

    if revision_requested:
        if current_content is None or feedback is None:
            raise ValueError(
                "A revision requires both current_content and feedback."
            )

        prompt = build_revision_prompt(
            topic=topic,
            content_type=content_type,
            context=context,
            current_content=current_content,
            feedback=feedback,
        )

        generation_mode = "revision"

    else:
        prompt = build_generation_prompt(
            topic=topic,
            content_type=content_type,
            context=context,
        )

        generation_mode = "new_draft"

    generated_content = generate_content(prompt)

    checker_results = run_content_checker(
        generated_content=generated_content,
        content_type=content_type,
    )

    return {
        "generated_content": generated_content,
        "selected_documents": selected_documents,
        "context": context,
        "checker_results": checker_results,
        "generation_mode": generation_mode,
    }


if __name__ == "__main__":
    test_result = generate_content_pipeline(
        topic="Why AI projects fail",
        content_type="linkedin_post",
    )

    print("\nGenerated Content:\n")
    print(test_result["generated_content"])

    if test_result["checker_results"] is not None:
        print("\nLinkedIn Quality Check:\n")
        print(test_result["checker_results"])