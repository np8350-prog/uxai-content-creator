"""
review.py

This module manages the human review checkpoint.

It does not call the LLM and does not generate content.

Its only responsibility is to collect the reviewer's decision:
1. Approve the draft.
2. Request an edit.
3. Reject the draft.
"""

from typing import Optional


def ask_for_edit_feedback() -> str:
    """
    Ask the reviewer to describe the requested changes.

    Returns
    -------
    str
        Non-empty reviewer feedback.
    """

    while True:
        feedback = input(
            "\nDescribe the changes you would like:\n"
        ).strip()

        if feedback:
            return feedback

        print("\nFeedback cannot be empty.")


def ask_after_rejection() -> str:
    """
    Ask what should happen after a draft is rejected.

    Returns
    -------
    str
        One of:
        - new_draft
        - change_inputs
        - exit
    """

    while True:
        print("\nWhat would you like to do next?")
        print("1. Generate another draft")
        print("2. Change the topic or content type")
        print("3. Exit")

        choice = input(
            "\nChoose option 1, 2, or 3: "
        ).strip()

        if choice == "1":
            return "new_draft"

        if choice == "2":
            return "change_inputs"

        if choice == "3":
            return "exit"

        print("\nInvalid option. Please enter 1, 2, or 3.")


def review_content(generated_content: str) -> dict:
    """
    Collect the human reviewer's decision.

    Parameters
    ----------
    generated_content : str
        Draft currently under review.

    Returns
    -------
    dict
        Review result containing:
        - status
        - final_content
        - feedback
        - next_action
    """

    while True:
        print("\n" + "=" * 60)
        print("HUMAN REVIEW")
        print("=" * 60)

        print("1. Approve")
        print("2. Request edits")
        print("3. Reject")

        choice = input(
            "\nChoose option 1, 2, or 3: "
        ).strip()

        # Approve the current draft.
        if choice == "1":
            return {
                "status": "approved",
                "final_content": generated_content,
                "feedback": None,
                "next_action": "finish",
            }

        # Ask the pipeline to revise the current draft.
        if choice == "2":
            feedback = ask_for_edit_feedback()

            return {
                "status": "edit_requested",
                "final_content": None,
                "feedback": feedback,
                "next_action": "revise",
            }

        # Reject the current draft and ask what happens next.
        if choice == "3":
            print("\nThe current draft has been rejected.")

            next_action = ask_after_rejection()

            return {
                "status": "rejected",
                "final_content": None,
                "feedback": None,
                "next_action": next_action,
            }

        print("\nInvalid option. Please enter 1, 2, or 3.")