"""
test_case_study_summary.py

This file tests the case-study summary prompt template.

We are checking this flow:

1. Create a case-study topic.
2. Create dummy brand context.
3. Use case_study_summary() to build a structured prompt.
4. Send that prompt to the LLM.
5. Print the generated case-study summary.
"""

from llm_integration import generate_content
from prompt_templates import case_study_summary


# This is the topic for the case-study style output.
topic = "Improving user trust in an AI-powered customer support tool"


# This is simple test context.
# Later, Stage C will replace this with selected knowledge-base content.
dummy_context = """
The brand focuses on AI strategy, UX research, ethical product design,
and helping teams build AI tools that are understandable, trustworthy,
and useful for real users.
"""


# Build the final case-study prompt.
prompt = case_study_summary(topic, dummy_context)


# Send the prompt to the LLM.
result = generate_content(prompt)


# Print the generated case-study summary.
print(result)