"""
app.py

Flask web app for the UXAI Content Creator.

Wires the existing pipeline (content_pipeline.py, review.py) into
a real browser-based flow, matching the approved design:
Topic -> Content Type -> Generated Draft -> Human Review.

This does not replace main.py (the CLI version). It's an
additional interface over the same underlying pipeline logic.
"""

import re
import html as html_lib

from flask import Flask, render_template, request, redirect, url_for, session, Response
from review import log_review_decision, LOG_PATH
from content_pipeline import generate_content_pipeline


app = Flask(__name__)
app.secret_key = "dev-only-secret-change-if-deploying"


CONTENT_TYPES = [
    {
        "key": "thought_leadership",
        "title": "Thought Leadership",
        "desc": "Long-form argument with a clear thesis, for deep, considered takes.",
    },
    {
        "key": "linkedin_post",
        "title": "LinkedIn Post",
        "desc": "Short, hook-driven, mobile-first. One idea, one takeaway.",
    },
    {
        "key": "case_study_summary",
        "title": "Case Study Summary",
        "desc": "Structured Problem / Approach / Insight / Impact format.",
    },
]

TYPE_LABELS = {c["key"]: c["title"] for c in CONTENT_TYPES}


CASE_STUDY_LABELS = {
    "problem": "pill-red",
    "approach": "pill-blue",
    "insight": "pill-green",
    "result or potential impact": "pill-yellow",
    "result": "pill-yellow",
}


def format_inline(text):
    """Escape HTML, then convert **bold** and *italic* to real tags."""

    text = html_lib.escape(text)
    text = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"\*(.+?)\*", r"<em>\1</em>", text)
    return text


def format_draft_html(text, content_type):
    """
    Convert raw LLM draft text into styled HTML.

    Case study summaries get their section labels (Problem, Approach,
    Insight, Result or Potential Impact) turned into colored pills.
    All types get basic markdown (##, **, *) converted to real HTML.
    """

    text = text.strip()
    lines = text.split("\n")

    label_pattern = re.compile(
        r"^\*{0,2}(Problem|Approach|Insight|Result or Potential Impact|Result)\*{0,2}:?\s*$",
        re.IGNORECASE,
    )
    heading_pattern = re.compile(r"^#{1,3}\s+(.*)")

    html_parts = []
    buffer = []

    def flush_paragraph():
        if buffer:
            paragraph_text = " ".join(buffer).strip()
            if paragraph_text:
                html_parts.append(f"<p>{format_inline(paragraph_text)}</p>")
            buffer.clear()

    for raw_line in lines:
        line = raw_line.strip()

        if not line:
            flush_paragraph()
            continue

        label_match = label_pattern.match(line)
        if label_match and content_type == "case_study_summary":
            flush_paragraph()
            label_text = label_match.group(1)
            css_class = CASE_STUDY_LABELS.get(label_text.lower(), "pill-yellow")
            html_parts.append(
                f'<div class="section-pill {css_class}">{html_lib.escape(label_text)}</div>'
            )
            continue

        heading_match = heading_pattern.match(line)
        if heading_match:
            flush_paragraph()
            html_parts.append(f"<h3>{format_inline(heading_match.group(1))}</h3>")
            continue

        buffer.append(line)

    flush_paragraph()

    return "\n".join(html_parts)

@app.route("/download")
def download_draft():
    """Download the approved draft as a plain text file."""

    topic = session.get("topic", "content")
    content_type = session.get("content_type", "draft")
    draft = session.get("draft")

    if not draft:
        return redirect(url_for("topic_page"))

    safe_topic = re.sub(r"[^a-zA-Z0-9]+", "-", topic).strip("-").lower()
    filename = f"{safe_topic}-{content_type}.txt"

    return Response(
        draft,
        mimetype="text/plain",
        headers={"Content-Disposition": f"attachment; filename={filename}"},
    )



@app.route("/", methods=["GET", "POST"])
def topic_page():
    """Step 1: enter a content topic."""

    if request.method == "POST":
        topic = request.form.get("topic", "").strip()

        if topic:
            session["topic"] = topic
            return redirect(url_for("select_type_page"))

    return render_template("topic.html", topic=session.get("topic", ""))


@app.route("/select-type", methods=["GET", "POST"])
def select_type_page():
    """Step 2: choose a content format."""

    topic = session.get("topic")

    if not topic:
        return redirect(url_for("topic_page"))

    if request.method == "POST":
        content_type = request.form.get("content_type")

        if content_type in TYPE_LABELS:
            session["content_type"] = content_type
            return redirect(url_for("generating_page"))

    return render_template(
        "select_type.html",
        topic=topic,
        content_types=CONTENT_TYPES,
        selected=session.get("content_type"),
    )

@app.route("/generating")
def generating_page():
    """Loading screen shown before the actual generation call runs."""

    topic = session.get("topic")
    content_type = session.get("content_type")

    if not topic or not content_type:
        return redirect(url_for("topic_page"))

    return render_template(
        "generating.html",
        type_label=TYPE_LABELS[content_type],
        topic=topic,
    )
@app.route("/revising")
def revising_page():
    """Loading screen shown before a revision call runs."""

    topic = session.get("topic")
    content_type = session.get("content_type")
    feedback = session.get("pending_feedback")

    if not topic or not content_type or not feedback:
        return redirect(url_for("topic_page"))

    return render_template(
        "revising.html",
        type_label=TYPE_LABELS[content_type],
        feedback=feedback,
    )


@app.route("/generate-revision")
def generate_revision():
    """Runs the actual revision call, after the loading screen has painted."""

    topic = session.get("topic")
    content_type = session.get("content_type")
    draft = session.get("draft")
    feedback = session.get("pending_feedback")

    if not topic or not content_type or not draft or not feedback:
        return redirect(url_for("topic_page"))

    try:
        result = generate_content_pipeline(
            topic=topic,
            content_type=content_type,
            current_content=draft,
            feedback=feedback,
        )
    except Exception as error:
        return render_template("error.html", message=str(error))

    session["draft"] = result["generated_content"]
    session["checker"] = result.get("checker_results")
    session.pop("pending_feedback", None)

    return render_template(
        "draft.html",
        topic=topic,
        content_type=content_type,
        type_label=TYPE_LABELS[content_type],
        draft_html=format_draft_html(result["generated_content"], content_type),
        checker=result.get("checker_results"),
        revision_note=feedback,
    )

@app.route("/generate")
def generate_page():
    """Step 3: generate a draft using the real pipeline."""

    topic = session.get("topic")
    content_type = session.get("content_type")

    if not topic or not content_type:
        return redirect(url_for("topic_page"))

    try:
        result = generate_content_pipeline(
            topic=topic,
            content_type=content_type,
        )
    except Exception as error:
        return render_template("error.html", message=str(error))

    session["draft"] = result["generated_content"]
    session["checker"] = result.get("checker_results")

    return render_template(
        "draft.html",
        topic=topic,
        content_type=content_type,
        type_label=TYPE_LABELS[content_type],
        draft_html=format_draft_html(result["generated_content"], content_type),
        checker=result.get("checker_results"),
    )


@app.route("/review", methods=["POST"])
def review_action():
    """Step 4: handle Approve / Request edits / Reject."""

    topic = session.get("topic")
    content_type = session.get("content_type")
    draft = session.get("draft")

    if not topic or not content_type or not draft:
        return redirect(url_for("topic_page"))

    action = request.form.get("action")

    if action == "approve":
        log_review_decision(topic, content_type, "approved")
        return render_template(
            "approved.html",
            draft_html=format_draft_html(draft, content_type),
        )

    if action == "reject":
        log_review_decision(topic, content_type, "rejected")
        return render_template("rejected.html", topic=topic, content_type=content_type)

    if action == "request_edits":
        feedback = request.form.get("feedback", "").strip()

        if not feedback:
            return render_template(
                "draft.html",
                topic=topic,
                content_type=content_type,
                type_label=TYPE_LABELS[content_type],
                draft_html=format_draft_html(draft, content_type),
                checker=session.get("checker"),
                edit_error="Please describe the changes you'd like.",
            )

        log_review_decision(topic, content_type, "edit_requested", feedback)
        session["pending_feedback"] = feedback
        return redirect(url_for("revising_page"))

    return redirect(url_for("topic_page"))

@app.route("/reject-choice", methods=["POST"])
def reject_choice():
    """Handle the user's choice after a rejection."""

    topic = session.get("topic")
    content_type = session.get("content_type")
    choice = request.form.get("choice")

    if not topic or not content_type:
        return redirect(url_for("topic_page"))

    if choice == "regenerate":
        return redirect(url_for("generating_page"))

    if choice == "change_type":
        session.pop("content_type", None)
        session.pop("draft", None)
        return redirect(url_for("select_type_page"))

    if choice == "change_topic":
        session.pop("topic", None)
        session.pop("draft", None)
        return redirect(url_for("topic_page"))

    if choice == "change_both":
        session.pop("topic", None)
        session.pop("content_type", None)
        session.pop("draft", None)
        return redirect(url_for("topic_page"))

    if choice == "exit":
        session.clear()
        return redirect(url_for("topic_page"))

    return redirect(url_for("topic_page"))

@app.route("/new")
def new_draft():
    """Clear session and start over from the topic screen."""

    session.clear()
    return redirect(url_for("topic_page"))

@app.route("/log")
def review_history():
    """Show the review log: every approve/edit/reject decision made."""

    entries = []

    if LOG_PATH.exists():
        raw = LOG_PATH.read_text(encoding="utf-8")
        blocks = raw.split("## ")[1:]

        for block in blocks:
            lines = block.strip().split("\n")
            entry = {"timestamp": lines[0].strip()}

            for line in lines[1:]:
                line = line.strip()
                if line.startswith("- Topic:"):
                    entry["topic"] = line.replace("- Topic:", "").strip()
                elif line.startswith("- Content type:"):
                    entry["content_type"] = line.replace("- Content type:", "").strip()
                elif line.startswith("- Decision:"):
                    entry["decision"] = line.replace("- Decision:", "").strip()
                elif line.startswith("- Feedback:"):
                    entry["feedback"] = line.replace("- Feedback:", "").strip()

            entries.append(entry)

    entries.reverse()

    return render_template("log.html", entries=entries)

if __name__ == "__main__":
    app.run(debug=True, port=5000)