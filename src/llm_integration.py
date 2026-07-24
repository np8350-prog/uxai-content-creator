"""
llm_integration.py

This module handles communication with the OpenAI API.

It receives a complete prompt, sends it to the selected model,
and returns the generated text.
"""

import os

from dotenv import load_dotenv
from openai import OpenAI


# Load environment variables from the .env file.
load_dotenv()


def create_openai_client() -> OpenAI:
    """
    Create and return an OpenAI client.

    Returns
    -------
    OpenAI
        Configured OpenAI client.

    Raises
    ------
    ValueError
        If OPENAI_API_KEY is not available.
    """

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise ValueError(
            "OPENAI_API_KEY was not found. "
            "Add it to your .env file before running the application."
        )

    return OpenAI(api_key=api_key)


def generate_content(prompt: str) -> str:
    """
    Send a prompt to the LLM and return its text response.

    Parameters
    ----------
    prompt : str
        Complete instruction sent to the model.

    Returns
    -------
    str
        Generated text.

    Raises
    ------
    ValueError
        If the prompt is empty or the model returns no text.
    RuntimeError
        If the API request fails.
    """

    if not prompt or not prompt.strip():
        raise ValueError("The prompt cannot be empty.")

    client = create_openai_client()

    # Use the model defined in .env.
    # gpt-4.1-mini is used as a practical default.
    model = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")

    try:
        response = client.responses.create(
            model=model,
            input=prompt.strip(),
        )

    except Exception as error:
        raise RuntimeError(
            f"The OpenAI request failed: {error}"
        ) from error

    generated_text = response.output_text

    if not generated_text or not generated_text.strip():
        raise ValueError("The model returned an empty response.")

    return generated_text.strip()