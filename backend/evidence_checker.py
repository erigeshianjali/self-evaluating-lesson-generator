
import re


def get_words(text):
    """Convert text into a set of lowercase words."""

    return set(re.findall(r"\b[a-zA-Z]{3,}\b", text.lower()))


def check_evidence(claims, reference_text):

    results = []

    reference_words = get_words(reference_text)

    for claim in claims:

        claim_words = get_words(claim)

        if not claim_words:
            results.append({
                "claim": claim,
                "status": "NEEDS_REVIEW",
                "feedback": "No meaningful words found."
            })
            continue

        # Find words shared by the claim and reference
        matching_words = claim_words.intersection(reference_words)

        # Calculate the percentage of matching words
        match_percentage = (
            len(matching_words) / len(claim_words)
        ) * 100

        if match_percentage >= 50:
            status = "POTENTIAL_SUPPORT"
            feedback = (
                "Some matching terms were found. "
                "A human must check the actual meaning."
            )
        else:
            status = "NEEDS_REVIEW"
            feedback = (
                "Insufficient word overlap. "
                "Check this claim against a trusted source."
            )

        results.append({
            "claim": claim,
            "status": status,
            "matching_words": sorted(matching_words),
            "match_percentage": round(match_percentage, 2),
            "feedback": feedback
        })

    return {
        "overall_status": "PENDING",
        "results": results,
        "message": (
            "Text matching is not factual verification. "
            "Human review is required before approval."
        )
    }
