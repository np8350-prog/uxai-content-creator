"""
main.py

Entry point for the UXAI Content Creator.

This module controls the user experience and coordinates:
- topic selection
- content-type selection
- draft generation
- automatic checking
- human review
- revision
- rejection
- generation of alternative drafts
"""

from content_pipeline import generate_content_pipeline
from review import review_content


CONTENT_TYPE_LABELS = {
    "thought_leadership": "Thought Leadership",
    "linkedin_post": "LinkedIn Post",
    "case_study_summary": "Case Study Summary",
}


def ask_for_topic() -> str:
    """
    Ask the user for a non-empty content topic.

    Returns
    -------
    str
        Content topic.
    """

    while True:
        topic = input(
            "\nEnter the content topic: "
        ).strip()

        if topic:
            return topic

        print("\nThe topic cannot be empty.")


def select_content_type() -> str:
    """
    Ask the user to choose a content format.

    Returns
    -------
    str
        Internal content-type value used by the pipeline.
    """

    options = {
        "1": "thought_leadership",
        "2": "linkedin_post",
        "3": "case_study_summary",
    }

    while True:
        print("\nSelect a content type:")
        print("1. Thought Leadership")
        print("2. LinkedIn Post")
        print("3. Case Study Summary")

        choice = input(
            "\nChoose option 1, 2, or 3: "
        ).strip()

        if choice in options:
            return options[choice]

        print("\nInvalid option. Please enter 1, 2, or 3.")


def display_current_request(
    topic: str,
    content_type: str,
) -> None:
    """
    Display the user's current content request.
    """

    content_label = CONTENT_TYPE_LABELS.get(
        content_type,
        content_type,
    )

    print("\n" + "=" * 60)
    print("CURRENT REQUEST")
    print("=" * 60)
    print(f"Topic: {topic}")
    print(f"Content type: {content_label}")


def display_generated_draft(
    pipeline_result: dict,
    draft_number: int,
) -> None:
    """
    Display generated content and checker results.

    Parameters
    ----------
    pipeline_result : dict
        Result returned by the content pipeline.

    draft_number : int
        Sequential number of the draft.
    """

    generation_mode = pipeline_result.get(
        "generation_mode",
        "new_draft",
    )

    if generation_mode == "revision":
        title = f"REVISED DRAFT #{draft_number}"
    else:
        title = f"GENERATED DRAFT #{draft_number}"

    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(pipeline_result["generated_content"])

    checker_results = pipeline_result.get(
        "checker_results"
    )

    if checker_results is not None:
        print("\n" + "=" * 60)
        print("LINKEDIN QUALITY CHECK")
        print("=" * 60)
        print(checker_results)


def generate_draft(
    topic: str,
    content_type: str,
    current_content: str | None = None,
    feedback: str | None = None,
) -> dict | None:
    """
    Generate or revise a draft safely.

    Returns
    -------
    dict | None
        Pipeline result, or None if generation fails.
    """

    if current_content is not None:
        print("\nRevising the draft. Please wait...")
    else:
        print("\nGenerating content. Please wait...")

    try:
        return generate_content_pipeline(
            topic=topic,
            content_type=content_type,
            current_content=current_content,
            feedback=feedback,
        )

    except ValueError as error:
        print(f"\nInput error: {error}")
        return None

    except RuntimeError as error:
        print(f"\nGeneration error: {error}")
        return None

    except Exception as error:
        print(
            "\nAn unexpected error occurred while "
            f"generating content: {error}"
        )
        return None


def ask_after_generation_error() -> str:
    """
    Ask what the user wants to do after generation fails.

    Returns
    -------
    str
        retry, change_inputs, or exit.
    """

    while True:
        print("\nWhat would you like to do?")
        print("1. Try again")
        print("2. Change the topic or content type")
        print("3. Exit")

        choice = input(
            "\nChoose option 1, 2, or 3: "
        ).strip()

        if choice == "1":
            return "retry"

        if choice == "2":
            return "change_inputs"

        if choice == "3":
            return "exit"

        print("\nInvalid option. Please enter 1, 2, or 3.")


def main() -> None:
    """
    Run the complete UXAI Content Creator workflow.
    """

    print("=" * 60)
    print("UXAI CONTENT CREATOR")
    print("=" * 60)

    topic = ask_for_topic()
    content_type = select_content_type()

    draft_number = 1

    # This variable stores revision feedback.
    pending_feedback = None

    # This variable stores the draft that must be revised.
    content_to_revise = None

    while True:
        display_current_request(
            topic=topic,
            content_type=content_type,
        )

        pipeline_result = generate_draft(
            topic=topic,
            content_type=content_type,
            current_content=content_to_revise,
            feedback=pending_feedback,
        )

        # Handle generation errors without crashing.
        if pipeline_result is None:
            error_action = ask_after_generation_error()

            if error_action == "retry":
                continue

            if error_action == "change_inputs":
                topic = ask_for_topic()
                content_type = select_content_type()
                draft_number = 1
                content_to_revise = None
                pending_feedback = None
                continue

            print("\nApplication closed.")
            break

        generated_content = pipeline_result[
            "generated_content"
        ]

        display_generated_draft(
            pipeline_result=pipeline_result,
            draft_number=draft_number,
        )

        review_result = review_content(
            generated_content
        )

        # --------------------------------------------------
        # APPROVE
        # --------------------------------------------------

        if review_result["status"] == "approved":
            print("\n" + "=" * 60)
            print("FINAL APPROVED CONTENT")
            print("=" * 60)
            print(review_result["final_content"])

            print("\nContent workflow completed.")
            break

        # --------------------------------------------------
        # EDIT
        # --------------------------------------------------

        if review_result["status"] == "edit_requested":
            content_to_revise = generated_content
            pending_feedback = review_result["feedback"]

            draft_number += 1
            continue

        # --------------------------------------------------
        # REJECT
        # --------------------------------------------------

        if review_result["status"] == "rejected":
            next_action = review_result["next_action"]

            # Generate an alternative draft using the same
            # topic and content type.
            if next_action == "new_draft":
                content_to_revise = None
                pending_feedback = None
                draft_number += 1
                continue

            # Return to topic and content-type selection.
            if next_action == "change_inputs":
                topic = ask_for_topic()
                content_type = select_content_type()

                draft_number = 1
                content_to_revise = None
                pending_feedback = None
                continue

            # Exit cleanly.
            print("\nApplication closed.")
            break


if __name__ == "__main__":
    main()