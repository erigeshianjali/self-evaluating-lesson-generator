import re

CRITERIA = (
    "accuracy_and_grounding",
    "beginner_friendly",
    "teaches_by_example",
    "no_unexplained_jargon",
    "covers_key_points",
    "coherent_flow",
)

def evaluate_lesson(lesson: str, accuracy_status: str = "PENDING") -> dict:
    """Evaluate a lesson against six fixed criteria.

    accuracy_status must be supplied by a human verification workflow.
    Text matching alone must never set it to PASS.
    """
    results = {}

    if accuracy_status not in {"PASS", "FAIL", "PENDING"}:
        accuracy_status = "PENDING"

    results["accuracy_and_grounding"] = {
        "status": accuracy_status,
        "feedback": (
            "A human reviewer marked the claims as checked against the supplied source."
            if accuracy_status == "PASS"
            else "Factual claims have not been independently verified. Human review is required."
        ),
    }

    sentences = [s.strip() for s in re.split(r"[.!?]+", lesson) if s.strip()]
    long_sentences = [s for s in sentences if len(s.split()) > 30]
    results["beginner_friendly"] = {
        "status": "FAIL" if long_sentences else "PASS",
        "feedback": "Some sentences are longer than 30 words." if long_sentences else "Sentences are reasonably short.",
    }

    results["teaches_by_example"] = {
        "status": "PASS" if "example" in lesson.lower() else "FAIL",
        "feedback": "Example section found." if "example" in lesson.lower() else "Add a practical example.",
    }

    jargon = ("embedding", "vector database", "retriever")
    lower = lesson.lower()
    unexplained = [
        term for term in jargon
        if term in lower
        and f"{term} means" not in lower
        and f"{term} is" not in lower
    ]
    results["no_unexplained_jargon"] = {
        "status": "FAIL" if unexplained else "PASS",
        "feedback": "Explain these terms: " + ", ".join(unexplained) if unexplained else "No known unexplained jargon detected.",
    }

    required = ("definition", "importance", "how it works", "advantages", "limitations")
    missing = [heading for heading in required if heading not in lower]
    results["covers_key_points"] = {
        "status": "FAIL" if missing else "PASS",
        "feedback": "Missing sections: " + ", ".join(missing) if missing else "All required sections found.",
    }

    has_intro = "introduction" in lower
    has_conclusion = "conclusion" in lower
    results["coherent_flow"] = {
        "status": "PASS" if has_intro and has_conclusion else "FAIL",
        "feedback": "Introduction and conclusion found." if has_intro and has_conclusion else "Add an introduction and conclusion.",
    }
    return results
