# Prompt Iteration Log

**Project:** AI Content Creator  
**Stage:** C – Output Evaluation & Prompt Iteration  
**Status:** Implemented and Validated

---

# Purpose

This review evaluates how the current prompt templates behave once connected to the knowledge base and used to generate real content.

The current implementation already provides a solid foundation. It separates content types, retrieves contextual information from the knowledge base and consistently generates the expected outputs.

Our review focused on a single question:

> **Once the model knows *what* to generate, are we giving it enough editorial guidance to consistently produce the kind of content we actually want?**

After reviewing multiple outputs, we found that most opportunities for improvement were editorial rather than technical.

The generated content is technically correct, but its quality and consistency vary depending on the topic, audience and content format.

This document captures our findings, documents the implemented prompt refinements and records the results of the final validation.

The implemented refinements leave the current architecture, retrieval process and knowledge base unchanged.

---

# Evaluation Framework

To keep the review consistent, all generated outputs were evaluated using the same criteria across the three prompt templates.

| Evaluation Area | Why it Matters |
|-----------------|----------------|
| **Audience Fit** | Does the content adapt to the intended reader, or only describe the topic? |
| **Message Clarity** | Is there one clear takeaway, or are multiple ideas competing for attention? |
| **Readability** | Is the content easy to scan and consume in a digital environment? |
| **Platform Behaviour** | Does the structure reflect how the content will actually be consumed? |
| **Context Transformation** | Does the model synthesise the retrieved knowledge instead of reproducing it? |
| **Trust & Grounding** | Are factual claims clearly supported by the available context? |
| **Content Differentiation** | Does each template produce recognisably different outputs? |

Findings were cross-checked against an independent LLM review to reduce blind spots and validate our observations before proposing any refinements.

---

# Initial Prompt Evaluation

The first evaluation focused on how each prompt template behaved when generating multiple outputs using different topics and the same knowledge base.

Rather than assessing writing quality in isolation, we looked for recurring patterns that could explain differences in consistency across generations.

| Template | What Worked | Opportunity Identified |
|-----------|-------------|------------------------|
| **Thought Leadership** | Produced structured long-form content with a professional consulting tone. | The prompt defines the topic but leaves the audience, central thesis and information hierarchy largely to the model, resulting in variable depth and focus. |
| **LinkedIn Post** | Successfully generated professional social content using the retrieved context. | The prompt does not explicitly define platform-specific writing behaviour. Mobile readability, hook quality, visual rhythm and "See more" optimisation depend heavily on the model's own interpretation. |
| **Case Study Summary** | The predefined structure consistently generated clear and well-organised summaries. | The narrative occasionally prioritised describing activities over communicating transformation, business value and measurable outcomes. |

---

# Key Observations

## 1. Retrieved context was not always transformed

The knowledge base provides relevant expertise, terminology and consulting context.

However, the prompts do not explicitly distinguish between using the retrieved information as a source of knowledge and reproducing its wording or structure.

As a result, some outputs remained closer to a summary than to an original piece of content.

---

## 2. Platform behaviour remained implicit

This was most noticeable in the LinkedIn template.

Although the prompt specifies the content type, it does not explain how LinkedIn content is typically consumed.

Key editorial behaviours are therefore left to the model, including:

- writing for mobile-first reading;
- opening with a strong hook;
- communicating the main idea before the "See more" break;
- maintaining visual rhythm through short paragraphs;
- avoiding generic engagement prompts.

These elements have a direct impact on readability and perceived quality.

---

## 3. Readability depended on interpretation

Instructions such as *"keep it concise"* or *"make it easy to read"* are subjective and may be interpreted differently across generations.

Replacing subjective guidance with observable writing behaviours—such as active voice, concise paragraphs, white space and one central idea per section—should improve consistency while reducing cognitive load.

---

## 4. Grounding was applied unevenly

The Case Study template already includes explicit guidance to avoid unsupported metrics or fabricated claims.

Applying the same grounding principles across every content type would create a more consistent editorial standard and reinforce trust throughout the application.


---

# Prompt Iterations

The review identified a series of refinements intended to improve editorial consistency without modifying the existing prompt architecture.

Each iteration addresses a specific observation identified during the evaluation phase.

| Iteration | Observation | Implemented Refinement | Validated Impact |
|-----------|-------------|------------------------|------------------|
| **1. Audience-first writing** | The prompts define the author but not the intended reader or communication objective. | Add a short planning step asking the model to identify the target audience, the core message and the desired reader outcome before writing. | Better relevance, more appropriate terminology and stronger communication. |
| **2. One core message** | Some outputs attempted to cover multiple ideas with equal importance. | Encourage the model to prioritise a single takeaway and remove supporting information that does not reinforce it. | More focused, concise and memorable content. |
| **3. Shared Editorial Guidelines** | Editorial behaviour is distributed across templates and often inferred by the model. | Introduce a reusable editorial layer shared by every content type before the format-specific instructions. | Greater consistency while keeping individual templates specialised. |
| **4. Context transformation** | Retrieved content occasionally resembled a summary of the knowledge base. | Explicitly instruct the model to use the retrieved context as a source of expertise, examples and terminology while synthesising original content. | Better use of the knowledge base and more differentiated outputs. |
| **5. UX writing principles** | General instructions such as "keep it concise" remain open to interpretation. | Replace subjective guidance with observable writing behaviours such as active voice, concise paragraphs, white space and clear information hierarchy. | Improved readability and lower cognitive load. |
| **6. Mobile-first behaviour** *(LinkedIn)* | Platform-specific reading behaviour is not explicitly defined. | Add guidance for strong hooks, visual rhythm, concise paragraphs, communicating the main idea before the "See more" break and avoiding forced engagement. | Better adaptation to LinkedIn consumption patterns and improved mobile readability. |
| **7. Trust & grounding** | Grounding rules are stronger in the Case Study template than in the other formats. | Apply the same factual grounding principles across every template, preserving quantitative information and avoiding unsupported claims. | Greater consistency and stronger credibility across all generated content. |
| **8. Semantic organisation** *(Thought Leadership)* | Long-form articles rely on the model to organise information without additional guidance. | Encourage a clear thesis, logical information hierarchy and descriptive section headings. | Better readability and improved suitability for long-form publishing and AI-assisted search (SEO/GEO). |

---

# Why a Shared Editorial Layer?

The review showed that the three prompt templates already define their respective content formats effectively.

However, they also share a common set of editorial expectations that are currently repeated, partially defined or left to the model's interpretation.

Introducing a shared Editorial Guidelines section allows these principles to be defined once and reused across every template.

This keeps responsibilities clearly separated.

| Shared Editorial Guidelines | Format-specific Requirements |
|-----------------------------|------------------------------|
| Define **how** the model should write. | Define **what** each content type should produce. |
| Audience adaptation | Thought Leadership structure |
| Core message | LinkedIn behaviour |
| Readability | Case Study structure |
| Trust & grounding | Platform-specific constraints |
| Context transformation | Format-specific objectives |

This approach reduces duplication, simplifies maintenance and provides a consistent editorial foundation without changing the existing retrieval strategy or application workflow.

---

# Implemented Prompt Changes

The implemented refinements preserve the existing prompt templates while introducing a shared editorial layer and strengthening the format-specific instructions where appropriate.

## Shared change (applies to all templates)

### Previous structure

```text
Role
↓
Topic
↓
Knowledge Base Context
↓
Format-specific Requirements
```

### Implemented structure

```text
Role
↓
Topic
↓
Knowledge Base Context
↓
Shared Editorial Guidelines
↓
Format-specific Requirements
```

The Shared Editorial Guidelines define **how** the model should write.

The format-specific requirements continue defining **what** each content type should produce.

This separation reduces prompt duplication while keeping each template focused on its specific purpose.

---

## Thought Leadership

| Previous behavior | Proposed refinement |
|-------------------|---------------------|
| Context is followed directly by format-specific instructions. | Insert the Shared Editorial Guidelines immediately after the retrieved context. |
| The prompt relies on the model to define the audience and central argument. | Add guidance to identify the target audience, establish one clear thesis and conclude with a practical takeaway. |
| Long-form structure is left largely to the model. | Encourage descriptive headings and a logical information hierarchy to improve readability and semantic organisation. |

---

## LinkedIn Post

| Previous behavior | Proposed refinement |
|-------------------|---------------------|
| Context is followed directly by format-specific instructions. | Insert the Shared Editorial Guidelines immediately after the retrieved context. |
| Platform-specific writing behaviour is mostly inferred by the model. | Add guidance for mobile-first reading, concise paragraphs, visual rhythm and communicating the main idea before the "See more" break. |
| Openings and endings vary across generations. | Define recommended hook patterns and encourage a natural closing aligned with the message rather than generic engagement prompts. |
| No suggested output length. | Recommend an approximate range of 900–1300 characters while prioritising clarity over length. |

---

## Case Study Summary

| Previous behavior | Proposed refinement |
|-------------------|---------------------|
| Existing structure consistently produces well-organised summaries. | Preserve the current structure. |
| Grounding rules are limited to this template. | Move factual grounding principles into the Shared Editorial Guidelines so they apply consistently across every content type. |
| The narrative sometimes focuses on activities rather than outcomes. | Reinforce a transformation-based narrative and clearly distinguish actual results from expected impact. |


---

# Implementation

The refinements were implemented exclusively in `prompt_templates.py`.

No changes were required to:

- the knowledge base;
- the retrieval strategy;
- the application workflow;
- the content pipeline.

The updated prompts were validated using the same topic ("chatbot ux") across the three content templates to enable a direct before-and-after comparison.

The validation focused on:

1. audience adaptation;
2. message clarity;
3. platform-specific behaviour;
4. context transformation;
5. trust and factual grounding;
6. differentiation between content formats.

---

# Conclusion

The prompt iteration improved editorial consistency without changing the product architecture.

The shared Editorial Guidelines now provide a common writing standard across all templates, while the format-specific requirements continue to define the behaviour of Thought Leadership articles, LinkedIn posts and Case Study summaries.

The validation confirmed measurable improvements in thesis clarity, platform adaptation and factual grounding. The strongest improvement appeared in the Case Study template, where unsupported client outcomes were replaced with explicitly qualified statements based only on available evidence.

One observation remains for future iterations: when multiple pieces cover related topics, the same grounded statistic may appear repeatedly across different formats. While factually correct, this could reduce content variety over time and should be monitored if the application is used for continuous content production.

---

# Confirmed Results (Post-Implementation)

**Status:** Implemented and tested — 2026-07-27

The refinements proposed above were implemented in `prompt_templates.py` and tested against the same topic ("chatbot ux") across all three templates. Results below are real generations, not projected outcomes.

## Case Study Summary: the clearest before/after

**Before refinement**, the Result section stated an unverified claim as fact:
> "Clients report clearer user understanding of chatbot behavior, reduced frustration, and increased engagement."

This violated the template's own instruction not to invent statistics or client feedback. No such client existed; this was a hypothetical case study.

**After refinement**, the same section correctly named its own limitation instead of fabricating a result:
> "While specific metrics aren't available here, this approach directly targets the 80% shipped versus 31% production usage gap..."

This confirms Iteration 7 (Trust & grounding) and the "clarify actual results vs expected impact" requirement worked as intended. The model now distinguishes real data (the Gartner/S&P adoption stats, which are grounded in `industry_trends.md`) from unverified outcomes, instead of blending them together as equally factual.

## Thought Leadership: thesis and structure

**Before refinement**, the thesis was present but diffuse across six numbered lessons with no single throughline.

**After refinement**, the piece opens with one stated thesis ("chatbot UX is fundamentally a governance challenge, not a superficial UI one") and explicitly returns to it in the closing paragraph. It also surfaces one genuine trade-off (simplicity vs. control), as required by Iteration 1 and the new Thought Leadership Requirements.

## LinkedIn Post: hook and length

**Before refinement**, the opening was a direct statement, functional but not built around a defined hook pattern.

**After refinement**, the post opens with a stated misconception ("Most chatbot UX fails because it ignores the AI beneath the interface"), matching the required hook types (misconception, lesson learned, challenge, or observation). Length landed within the 900-1300 character target.

## Open item carried forward

The Gartner 80%/31% adoption stat now appears across all three formats when the topic overlaps. This is accurate and grounded, not fabricated, but worth monitoring: if the system generates many pieces on similar topics, the same statistic repeating across a content calendar could start to feel repetitive. Not a correctness issue, a variety issue to watch if this system is used for ongoing content, not just this project.