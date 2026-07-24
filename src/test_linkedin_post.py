"""
test_linkedin_post.py

This file tests the LinkedIn post prompt template.

We are checking this flow:

1. Create a topic.
2. Create dummy brand context.
3. Use linkedin_post() to build a LinkedIn-style prompt.
4. Send that prompt to the LLM.
5. Print the generated LinkedIn post.
"""

from llm_integration import generate_content
from prompt_templates import linkedin_post
from content_checker import check_linkedin_post


# The topic is what the LinkedIn post should discuss.
topic = "Why AI tools need better UX research before launch"


# This is simple test context.
# Later, Stage C will replace this with selected knowledge-base content.
dummy_context = """
The brand focuses on practical AI strategy, UX research, ethical design,
and helping teams make AI products clear, useful, and trustworthy.
"""


# Build the final LinkedIn prompt.
prompt = linkedin_post(topic, dummy_context)


# Send the prompt to the LLM.
result = generate_content(prompt)
check_result = check_linkedin_post(result)


# Print the LinkedIn-style result.
print("Generated LinkedIn Post:")
print(result)

print("\nLinkedIn Check Result:")
print(check_result)