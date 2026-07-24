"""
test_llm_connection.py

This file checks if llm_integration.py can successfully talk to the LLM.

We are not testing the full content creator yet.
We are only testing one small thing:
Can Python send a prompt and receive a response?
"""

from llm_integration import generate_content


# This is a very small test prompt.
# We keep it simple so we can clearly see if the API connection works.
test_prompt = "Write one short sentence about why UX matters in AI products."


# Send the test prompt to the LLM.
result = generate_content(test_prompt)


# Print the answer so we can see it in the terminal.
print(result)