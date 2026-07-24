"""
test_thought_leadership.py

This file tests the first prompt template.

We are checking this flow:

1. Create a topic.
2. Create dummy brand context.
3. Use thought_leadership() to build a full prompt.
4. Send that prompt to generate_content().
5. Print the LLM result.
"""

from llm_integration import generate_content
from prompt_templates import thought_leadership


# The topic is the subject we want the content to discuss.
topic = "Why UX teams should be involved early in AI product development"


# This is fake/simple context for testing.
# Later in Stage C, this context will come from your knowledge base.
dummy_context = """
The brand focuses on AI strategy, UX research, ethical product design,
and helping teams build AI products that are useful, understandable,
and human-centered.
"""


# Build the final prompt using our template function.
prompt = thought_leadership(topic, dummy_context)


# Send the prompt to the LLM and receive generated content.
result = generate_content(prompt)


# Print the result so we can inspect it in the terminal.
print(result)