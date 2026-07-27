"""
review.py

This module manages the human review checkpoint.

It does not call the LLM and does not generate content.

Its only responsibility is to collect the reviewer's decision:
1. Approve the draft.
2. Request an edit.
3. Reject the draft.
"""
from datetime import datetime
from pathlib import Path


LOG_PATH = (
    Path(__file__).resolve().parent.parent
    / "uniqueness_evidence"
    / "review_log.md"
)


def log_review_decision(topic, content_type, status, feedback=None):
    LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")

    entry = f"## {timestamp}\n"
    entry += f"- Topic: {topic}\n"
    entry += f"- Content type: {content_type}\n"
    entry += f"- Decision: {status}\n"

    if feedback:
        entry += f"- Feedback: {feedback}\n"

    entry += "\n"

    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, "a", encoding="utf-8") as f:
        if not file_exists:
            f.write("# Review Log\n\n")
            f.write("Every human review decision made while running the content pipeline, in order.\n\n")
        f.write(entry)



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


def ask_after_approval() -> str:
    """
    Ask what should happen after a draft is approved.

    Returns
    -------
    str
        One of:
        - new_request
        - exit
    """

    while True:
        print("\nThe draft has been approved.")
        print("\nWhat would you like to do?")
        print()
        print("1. Start a new draft")
        print("2. Exit")

        choice = input(
            "\nChoose option 1 or 2: "
        ).strip()

        # Start a new content request from the beginning.
        if choice == "1":
            return "new_request"

        # End the content creation workflow.
        if choice == "2":
            return "exit"

        print("\nInvalid option. Please enter 1 or 2.")


def ask_after_rejection() -> str:
    """
    Ask what should happen after a draft is rejected.

    Returns
    -------
    str
        One of:
        - new_draft
        - change_content_type
        - change_topic
        - change_both
        - exit
    """

    while True:
        print("\nWhat would you like to do?")
        print()
        print("1. Start a new draft")
        print("2. Change content type")
        print("3. Change topic")
        print("4. Change both")
        print("5. Exit")

        choice = input(
            "\nChoose option 1, 2, 3, 4, or 5: "
        ).strip()

        # Keep the same topic and content type, but generate a new draft.
        if choice == "1":
            return "new_draft"

        # Keep the same topic, but allow the user to select another content type.
        if choice == "2":
            return "change_content_type"

        # Keep the same content type, but ask the user for a new topic.
        if choice == "3":
            return "change_topic"

        # Ask the user for both a new topic and a new content type.
        if choice == "4":
            return "change_both"

        # End the content creation workflow.
        if choice == "5":
            return "exit"

        print("\nInvalid option. Please enter 1, 2, 3, 4, or 5.")


def review_content(generated_content: str, topic: str, content_type: str)-> dict:
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

        # Approve the current draft and ask whether
        # the user wants to start another request or exit.
        if choice == "1":
            log_review_decision(topic, content_type, "approved")
            next_action = ask_after_approval()

            return {
                "status": "approved",
                "final_content": generated_content,
                "feedback": None,
                "next_action": next_action,
            }

        # Return the requested feedback so main.py can revise the current draft.
        if choice == "2":
            feedback = ask_for_edit_feedback()

            log_review_decision(topic, content_type, "edit_requested", feedback)

            return {
                "status": "edit_requested",
                "final_content": None,
                "feedback": feedback,
                "next_action": "revise",
            }

        # Reject the current draft and collect the user's next action.
        if choice == "3":
            print("\nThe current draft has been rejected.")
            log_review_decision(topic, content_type, "rejected")


            next_action = ask_after_rejection()

            return {
                "status": "rejected",
                "final_content": None,
                "feedback": None,
                "next_action": next_action,
            }

        print("\nInvalid option. Please enter 1, 2, or 3.")